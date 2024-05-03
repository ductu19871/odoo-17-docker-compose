from odoo import api, fields, models


class AccountPartialReconcile(models.Model):
    _inherit = "account.partial.reconcile"


    def unlink(self):
        return super().unlink()
    


class AML(models.Model):
    _inherit = "account.move.line"


    def write(self, vals):
        if 'debit' in vals or 'credit' in vals:
            print ('kakak')
        return super().write(vals)