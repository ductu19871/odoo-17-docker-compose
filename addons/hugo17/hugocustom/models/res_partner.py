from odoo import api, fields, models


class ResPartner(models.Model):

    _inherit = "res.partner"

    address2 = fields.Text()    