from odoo import models, fields

class SaleDeliveryMethod(models.Model):
    _name = 'sale.delivery.method'
    _description = 'Sale Delivery Method'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Delivery Method', required=True, tracking=True)
    active = fields.Boolean(default=True, tracking=True)
    # Add more fields as needed