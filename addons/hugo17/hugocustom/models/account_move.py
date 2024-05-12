from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError


class AM(models.Model):
    _inherit = 'account.move'

    ndt_payment_ids = fields.One2many('account.payment', 'move_id')
    count_ndt_payment = fields.Integer(compute='_compute_count_ndt_payment')
    is_trigger = fields.Boolean()

    @api.depends('is_trigger')
    def _compute_payment_state(self):
        return super()._compute_payment_state()
    
    def recompute_payment_state(self, limit=0, offset=0, add_domain=[]):
        dm = [('move_type', 'in', ('out_invoice', 'in_invoice'))]
        dm +=add_domain
        account_moves = self.env['account.move'].search(dm, limit =limit, offset=offset)
        n_split = 1000
        for r in account_moves:
            r.write({'state': r.state})
    
    def _compute_count_ndt_payment(self):
        for r in self:
            r.count_ndt_payment = len(r.ndt_payment_ids)
        
   

    # @api.model
    # def _search_default_journal(self, journal_types):
    #     company_id = self._context.get('default_company_id', self.env.company.id)
    #     warehouse_id = self._context.get('overwrite_user_warehouse_id') or self.env.user.warehouse_id

    #     domain = [('company_id', '=', company_id), ('type', 'in', journal_types), ('warehouse_id','=', warehouse_id.id)]# custome only here
    #     journal = self.env['account.journal'].search(domain, limit=1)
    #     if journal:
    #         return journal
    #     else:
    #         return super(AM, self)._search_default_journal(journal_types)
        # journal = None
        # if self._context.get('default_currency_id'):
        #     currency_domain = domain + [('currency_id', '=', self._context['default_currency_id'])]
        #     journal = self.env['account.journal'].search(currency_domain, limit=1)

        # if not journal:
        #     journal = self.env['account.journal'].search(domain, limit=1)

        # if not journal:
        #     company = self.env['res.company'].browse(company_id)

        #     error_msg = _(
        #         "No journal could be found in company %(company_name)s for any of those types: %(journal_types)s",
        #         company_name=company.display_name,
        #         journal_types=', '.join(journal_types),
        #     )
        #     raise UserError(error_msg)

        # return journal

    # @api.model
    # def _get_default_journal(self):
    #     ''' Get the default journal.
    #     It could either be passed through the context using the 'default_journal_id' key containing its id,
    #     either be determined by the default type.
    #     '''
    #     move_type = self._context.get('default_move_type', 'entry')
    #     if move_type in self.get_sale_types(include_receipts=True):
    #         journal_types = ['sale']
    #     elif move_type in self.get_purchase_types(include_receipts=True):
    #         journal_types = ['purchase']
    #     else:
    #         journal_types = self._context.get('default_move_journal_types', ['general'])

    #     if self._context.get('default_journal_id'):
    #         journal = self.env['account.journal'].browse(self._context['default_journal_id'])

    #         if move_type != 'entry' and journal.type not in journal_types:
    #             raise UserError(_(
    #                 "Cannot create an invoice of type %(move_type)s with a journal having %(journal_type)s as type.",
    #                 move_type=move_type,
    #                 journal_type=journal.type,
    #             ))
    #     else:
    #         journal = self._search_default_journal(journal_types)

    #     return journal
