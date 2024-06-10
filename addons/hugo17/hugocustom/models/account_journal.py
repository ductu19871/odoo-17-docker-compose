from odoo import api, fields, models
from odoo.tools.misc import formatLang


class AJ(models.Model):

    _inherit = "account.journal"
    # warehouse_id = fields.Many2one('stock.warehouse')

    def _fill_bank_cash_dashboard_data(self, dashboard_data):
        res = super()._fill_bank_cash_dashboard_data(dashboard_data)
        currency = self.currency_id or self.company_id.currency_id
        account_sum = 100
        if res:
            res['account_balance_ndt'] = formatLang(self.env, currency.round(account_sum) + 0.0, currency_obj=currency)
        return res

    @api.model
    def set_payment_account_id(self):
        return
        adict = {'1124': 'account.1_bank', '1111': 'account.1_cash'}
        for aa_code, journal_xid in adict.items():
            jn = self.env.ref(journal_xid)
            bank_account = self.env['account.account'].search([('code','=', aa_code)], limit=1)
            lines = self.env['account.payment.method.line'].search([('journal_id', '=', jn.id)])
            lines.payment_account_id = bank_account

        