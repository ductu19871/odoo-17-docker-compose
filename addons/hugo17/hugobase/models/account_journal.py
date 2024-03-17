from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError


class AA(models.Model):
    _inherit = 'account.journal'

    @api.model_create_multi
    def create(self, vals):
        # for val in vals:
        #     if 'account_id' in val and val.get('account_id'):
        #         print(1)
        # if 'account_id' in vals:
        #     print (2222)
        return super().create(vals)


    def write(self, vals):
        if 'account_id' in vals:
            print (2222)
        return super().write(vals)
