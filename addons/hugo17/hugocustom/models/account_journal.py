from odoo import api, fields, models


class AJ(models.Model):

    _inherit = "account.journal"
    warehouse_id = fields.Many2one('stock.warehouse')