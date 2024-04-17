from odoo import api, fields, models


class NewModel(models.Model):

    _name = "ndt.webhook"
    data = fields.Char()