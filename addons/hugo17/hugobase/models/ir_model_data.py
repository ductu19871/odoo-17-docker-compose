# -*- coding: utf-8 -*-
from odoo import models, api, fields, _
# from odoo.exceptions import Warning, UserError
# from datetime import datetime, timedelta, date
# from odoo import SUPERUSER_ID
# import logging as _logger


class IMD(models.Model):
    _inherit = "ir.model.data"

    @api.model
    def noupdate_write(self, xml_ids, val):
        for xml_id in xml_ids:
            module, name =xml_id.split('.')
            imd= self.search([('module','=', module), ('name', '=', name)])
            imd.write({'noupdate': val})
            
    @api.model
    def noupdate_true(self, xml_ids):
        for xml_id in xml_ids:
            module, name =xml_id.split('.')
            imd= self.search([('module','=', module), ('name', '=', name)])
            imd.write({'noupdate': True})
            
    @api.model
    def noupdate_false(self, xml_ids):
        for xml_id in xml_ids:
            module, name =xml_id.split('.')
            imd= self.search([('module','=', module), ('name', '=', name)])
            imd.write({'noupdate': False})
