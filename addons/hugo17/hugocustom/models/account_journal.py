from odoo import api, fields, models
from odoo.tools.misc import formatLang


class AJ(models.Model):

    _inherit = "account.journal"
    # warehouse_id = fields.Many2one('stock.warehouse')

    def _cal_account_balance(self, dashboard_data):
        # account_ids = tuple(ac for ac in [self.default_debit_account_id.id, self.default_credit_account_id.id] if ac)
        account_ids = self.default_account_id
        if account_ids:
            # amount_field = 'aml.balance' if (not self.currency_id or self.currency_id == self.company_id.currency_id) else 'aml.amount_currency'
            # query = """SELECT sum(%s) FROM account_move_line aml
            #             LEFT JOIN account_move move ON aml.move_id = move.id
            #             WHERE aml.account_id in %%s
            #             AND move.date <= %%s AND move.state = 'posted';""" % (amount_field,)

            query="""select  aa.id, sum(balance) as sum_balance from account_move_line aml
                join account_account aa on aa.id = aml.account_id 
                join account_move move on move.id = aml.move_id
                where aa.id in %s AND move.date <= %s AND move.state = 'posted'
                group by aa.id
                """
            self.env.cr.execute(query, (tuple(account_ids.ids), fields.Date.context_today(self),))
            query_results = self.env.cr.dictfetchall()
            account_vs_account_balance = {i['id']:i['sum_balance'] for i in query_results}
            currency = self.currency_id or self.company_id.currency_id
            if query_results:
                for journal_id, v in dashboard_data.items():
                    if 'account_balance' in v:
                        account_sum = account_vs_account_balance.get(self.env['account.journal'].browse(journal_id).default_account_id.id,0)
                        v['account_balance_ndt'] = formatLang(self.env, currency.round(account_sum) + 0.0,
                                                                  currency_obj=currency)
                # account_sum = query_results[0].get('sum')

    def _fill_bank_cash_dashboard_data(self, dashboard_data):
        res = super()._fill_bank_cash_dashboard_data(dashboard_data)
        bank_cash_journals = self.filtered(lambda journal: journal.type in ('bank', 'cash'))
        bank_cash_journals._cal_account_balance(dashboard_data)
        # currency = self.currency_id or self.company_id.currency_id
        # account_sum = 100
        # for k,v in dashboard_data.items():
        #     if 'account_balance' in v:
        #         account_sum = 100
        #         v['account_balance_ndt'] = formatLang(self.env, currency.round(account_sum) + 0.0, currency_obj=currency)
        # if res:
        #     res['account_balance_ndt'] = formatLang(self.env, currency.round(account_sum) + 0.0, currency_obj=currency)
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

        