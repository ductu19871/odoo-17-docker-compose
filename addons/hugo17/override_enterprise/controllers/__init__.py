from odoo import models


class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        result = super(Http, self).session_info()
        result['expiration_date'] = "2029-11-01 12:00:00"
        return result