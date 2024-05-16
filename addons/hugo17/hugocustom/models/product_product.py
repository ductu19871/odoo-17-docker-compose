from odoo import api, fields, models


class PP(models.Model):

    _inherit = "product.product"

    
    
    # @api.model
    # def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
    #     if not self.env.su and (self.user_has_groups('base.group_user') and not self.user_has_groups('hugocustom.group_bypass_brand_categ_rule')):
    #         args += ['|', ('product_brand_id','=', False), ('product_brand_id','in',self.env.user.brand_ids.ids),
    #                  '|', ('categ_id','=', False), ('categ_id','child_of', self.env.user.categ_ids.ids),
    #                  ]
    #     return super(PP, self)._search(args, offset, limit, order, count=count, access_rights_uid=access_rights_uid)
    
    # @api.model
    # def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
    #     if not self.env.su and (self.user_has_groups('base.group_user') and not self.user_has_groups('hugocustom.group_bypass_brand_categ_rule')):
    #         domain += ['|', ('product_brand_id','=', False), ('product_brand_id','in',self.env.user.brand_ids.ids),
    #                  '|', ('categ_id','=', False), ('categ_id','child_of', self.env.user.categ_ids.ids),
    #                  ]
    #     return super(PP, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)
    
    # Thêm thông tin tồn kho
    def name_get(self):
        name_get_vals = super(PP, self).name_get()
        read_vals = self.read(['qty_available', 'virtual_available', 'incoming_qty', 'outgoing_qty'])
        new_res = [(name_get_val[0], '%s|%s|%s|%s|%s'%(name_get_val[1], read_val['qty_available'], read_val['virtual_available'],
                                         read_val['incoming_qty'], read_val['outgoing_qty'])) for name_get_val, read_val in zip(name_get_vals, read_vals)]
        return new_res
    
class PT(models.Model):
    _inherit = "product.template"

    warranty_months = fields.Integer(string='Bảo hành')
    # @api.model
    # def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
    #     if not self.env.su and (self.user_has_groups('base.group_user') and not self.user_has_groups('hugocustom.group_bypass_brand_categ_rule')):
    #         args += ['|', ('product_brand_id','=', False), ('product_brand_id','in',self.env.user.brand_ids.ids),
    #                  '|', ('categ_id','=', False), ('categ_id','child_of', self.env.user.categ_ids.ids),
    #                  ]
    #     return super(PT, self)._search(args, offset, limit, order, count=count, access_rights_uid=access_rights_uid)

    # @api.model
    # def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
    #     if not self.env.su and (self.user_has_groups('base.group_user') and not self.user_has_groups('hugocustom.group_bypass_brand_categ_rule')):
    #         domain += ['|', ('product_brand_id','=', False), ('product_brand_id','in',self.env.user.brand_ids.ids),
    #                  '|', ('categ_id','=', False), ('categ_id','child_of', self.env.user.categ_ids.ids),
    #                  ]
    #     return super(PT, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)