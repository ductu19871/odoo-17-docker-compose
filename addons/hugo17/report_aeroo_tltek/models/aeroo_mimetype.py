# -*- coding: utf-8 -*-
from odoo import fields, models

class ReportMimeType(models.Model):
    _name = 'aeroo.mimetype'
    _description = 'Report Mime-Types'

    name = fields.Char('Name', size=64, required=True, readonly=True)
    code = fields.Char('Code', size=16, required=True, readonly=True)
    compatible_types = fields.Char(
        'Compatible Mime-Types', size=128,
        readonly=True)
    filter_name = fields.Char('Filter Name', size=128, readonly=True)
