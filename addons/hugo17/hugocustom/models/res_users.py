# Copyright 2015-TODAY ForgeFlow
# - Jordi Ballester Alomar
# Copyright 2015-TODAY Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class ResUsers(models.Model):

    _inherit = "res.users"

    # brand_ids = fields.Many2many('product.brand', 'user_brand_rel',  'user_id', 'brand_id', 'Brands')
    categ_ids = fields.Many2many('product.category', 'user_categ_rel',  'user_id', 'categ_id', 'Product Categories')
    warehouse_ids = fields.Many2many('stock.warehouse', 'user_warehouse_rel',  'user_id', 'warehouse_id','Warehouses')
    journal_ids = fields.Many2many('account.journal', 'user_journal_rel',  'user_id', 'journal_id', 'Journal')
    warehouse_id = fields.Many2one('stock.warehouse')


    def _get_default_warehouse_id(self):
        if self.warehouse_id:
            return self.warehouse_id
        return super(ResUsers, self)._get_default_warehouse_id()
        
    def write(self, data):
        if 'brand_ids' in data or 'categ_ids' in data or 'warehouse_ids' in data or 'journal_ids' in data:
            self.clear_caches()
        res = super(ResUsers, self).write(data)
        return res

