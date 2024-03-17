# -*- coding: utf-8 -*-
from odoo import fields, models

class AerooFilenameLine(models.Model):
    _name = 'aeroo.filename.line'
    _order = 'sequence'
    _description = 'Aeroo Filename Line'

    sequence = fields.Integer()
    report_id = fields.Many2one(
        'ir.actions.report', 'Report', required=True, ondelete='cascade')
    company_id = fields.Many2one('res.company', 'Company')
    lang_id = fields.Many2one('res.lang', 'Language')
    filename = fields.Char(required=True)
