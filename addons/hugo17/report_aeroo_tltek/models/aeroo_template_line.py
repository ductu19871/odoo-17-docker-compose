# -*- coding: utf-8 -*-
import base64
from odoo import api, fields, models, tools


class AerooTemplateLine(models.Model):
    _name = 'aeroo.template.line'
    _order = 'sequence'
    _description = 'Aeroo Template Line'

    sequence = fields.Integer()
    report_id = fields.Many2one(
        'ir.actions.report', 'Report', required=True, ondelete='cascade')
    company_id = fields.Many2one('res.company', 'Company')
    lang_id = fields.Many2one('res.lang', 'Language')
    template_data = fields.Binary('Template', required=True)
    template_filename = fields.Char('File Name')

    def get_aeroo_template(self, record):
        return base64.b64decode(self.template_data)
