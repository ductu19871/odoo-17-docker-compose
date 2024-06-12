# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class HrContract(models.Model):
    _name = 'hr.contract'
    _inherit = ['hr.contract', 'documents.mixin']

    def _get_document_tags(self):
        return self.company_id.documents_hr_contracts_tags

    def _get_document_owner(self):
        return self.employee_id.user_id

    def _get_document_partner(self):
        return self.employee_id.work_contact_id

    def _get_document_folder(self):
        return self.company_id.documents_hr_folder

    def _check_create_documents(self):
        return self.company_id.documents_hr_settings and super()._check_create_documents()

    def _get_sign_request_folder(self):
        self.ensure_one()
        return self.company_id.documents_hr_folder

    @api.ondelete(at_uninstall=False)
    def _unlink_except_contract_signature_tag(self):
        # TODO: remove me in master
        return
