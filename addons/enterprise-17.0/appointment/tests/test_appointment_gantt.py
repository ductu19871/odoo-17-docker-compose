# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo.addons.mail.tests.common import mail_new_test_user
from odoo.tests import users
from .common import AppointmentCommon


class AppointmentGanttTestCommon(AppointmentCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partners = cls.env['res.partner'].create([{
            'name': 'gantt attendee 1'
        }, {
            'name': 'gantt attendee 2'
        }])

        # create some appointments and users to ensure they are not linked to anything else
        [cls.user_bob, cls.user_john] = [mail_new_test_user(
            cls.env,
            company_id=cls.company_admin.id,
            email='bob@aptgantt.lan',
            groups='base.group_user',
            name='bob',
            login='bob@aptgantt.lan',
        ), mail_new_test_user(
            cls.env,
            company_id=cls.company_admin.id,
            email='john@aptgantt.lan',
            groups='base.group_user',
            name='john',
            login='john@aptgantt.lan',
        )]
        cls.apt_users = cls.user_bob + cls.user_john

        cls.apt_types = cls.env['appointment.type'].create([{
            'appointment_tz': 'UTC',
            'name': 'bob apt type',
            'staff_user_ids': [(4, cls.user_bob.id)],
        }, {
            'appointment_tz': 'UTC',
            'name': 'nouser apt type',
            'staff_user_ids': [],
        }])

        cls.gantt_context = {'appointment_booking_gantt_show_all_resources': True}
        cls.gantt_domain = [('appointment_type_id', 'in', cls.apt_types.ids)]

class AppointmentGanttTest(AppointmentGanttTestCommon):
    @users('apt_manager')
    def test_default_assign_user_attendees(self):
        """
        1> To check, Single attendee should be set as an organizer by default.
        (This is typically applied when selecting a specific slot in the
        appointment kanban.)

        2> (special gantt case) The current user should be an attendee if
        he is set as the organizer.
        """
        # context while clicking the 'New' btn
        no_attendees_context = {
            'booking_gantt_create_record': True,
            'appointment_default_assign_user_attendees': True,
            'default_partner_ids': [],
        }

        # context while clicking the time slot of the staff user
        single_attendee_context = {
            **no_attendees_context,
            'default_partner_ids': [self.user_bob.partner_id.id],
        }

        # Case 1: Specify a single attendee, simulating clicking a slot on the gantt view
        event_with_partner = self.env['calendar.event'].with_context(single_attendee_context).create({
            'name': 'event with partner',
            'appointment_type_id': self.apt_types[0].id,
        })
        # Case 2: Create an appointment without specifying attendees
        event_without_partner = self.env['calendar.event'].with_context(no_attendees_context).create({
            'name': 'event without partner',
            'appointment_type_id': self.apt_types[0].id,
        })

        # Case 1 check
        self.assertEqual(
            event_with_partner.user_id,
            self.user_bob,
            "Single attendee should be set as an organizer by default",
        )
        # Case 2 check
        self.assertEqual(
            event_without_partner.user_id,
            self.apt_manager,
            "The current user should be an organizer",
        )
        self.assertEqual(
            event_without_partner.attendee_ids.partner_id,
            self.apt_manager.partner_id,
            "If we don't specify an attendee, the current user should be set as an attendee",
        )

    def test_gantt_empty_groups(self):
        """Check that the data sent to gantt includes the right groups in the context of appointments."""
        gantt_data = self.env['calendar.event'].with_context(self.gantt_context).get_gantt_data(
            self.gantt_domain, ['partner_ids'], {}
        )
        group_partner_ids = [group['partner_ids'][0] for group in gantt_data['groups']]
        self.assertIn(self.user_bob.partner_id.id, group_partner_ids,
                      'Staff assigned to a user-scheduled appointment type should be shown in the default groups')
        self.assertNotIn(self.user_john.partner_id.id, group_partner_ids,
                         'Staff not assigned to any appointment type should be hidden')

        # add john as a staff user of an appointment type -> in the default groups
        self.apt_types[1].staff_user_ids = self.user_john

        gantt_data = self.env['calendar.event'].with_context(self.gantt_context).get_gantt_data(
            self.gantt_domain, ['partner_ids'], {}
        )
        group_partner_ids = [group['partner_ids'][0] for group in gantt_data['groups']]
        self.assertIn(self.user_bob.partner_id.id, group_partner_ids)
        self.assertIn(self.user_john.partner_id.id, group_partner_ids)

        # have default appointment in context -> only show staff assigned to that type
        context = self.gantt_context | {'default_appointment_type_id': self.apt_types[0].id}
        gantt_data = self.env['calendar.event'].with_context(context).get_gantt_data(
            self.gantt_domain, ['partner_ids'], {}
        )
        group_partner_ids = [group['partner_ids'][0] for group in gantt_data['groups']]
        self.assertIn(self.user_bob.partner_id.id, group_partner_ids)
        self.assertNotIn(self.user_john.partner_id.id, group_partner_ids, 'Should only display staff assigned to the default apt type.')

    def test_gantt_hide_non_staff(self):
        """Check that only the attendees that are part of the staff are used to compute the gantt data.

        The other attendees, such as the website visitors that created the meeting,
        are excluded and should not be displayed as gantt rows.
        """
        meeting = self._create_meetings(
            self.apt_users[0],
            [(self.reference_monday, self.reference_monday + timedelta(hours=1), False)],
            self.apt_types[0].id
        )
        meeting.partner_ids += self.partners[0]
        gantt_data = self.env['calendar.event'].with_context(self.gantt_context).get_gantt_data(
            self.gantt_domain, ['partner_ids'], {}
        )
        group_partner_ids = [group['partner_ids'][0] for group in gantt_data['groups']]
        self.assertNotIn(self.partners[0].id, group_partner_ids, 'Attendees with no users should be hidden from the grouping.')
        self.assertIn(self.user_bob.partner_id.id, group_partner_ids)
        self.assertNotIn(self.user_john.partner_id.id, group_partner_ids)
        self.assertEqual(gantt_data['records'], [{'id': meeting.id}])

    def test_gantt_without_attendees(self):
        meeting = self._create_meetings(
            self.user_john[0],
            [(self.reference_monday, self.reference_monday + timedelta(hours=1), False)],
            self.apt_types[0].id
        )
        meeting.partner_ids = False
        gantt_data = self.env['calendar.event'].with_context(self.gantt_context).get_gantt_data(
            self.gantt_domain, ['partner_ids'], {}
        )
        group_partner_ids = [group['partner_ids'][0] for group in gantt_data['groups']]
        self.assertIn(self.user_bob.partner_id.id, group_partner_ids)
        self.assertNotIn(self.user_john.partner_id.id, group_partner_ids)
        self.assertEqual(gantt_data['records'], [{'id': meeting.id}])
