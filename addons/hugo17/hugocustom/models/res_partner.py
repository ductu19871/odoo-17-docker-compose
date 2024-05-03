from odoo import api, fields, models


class ResPartner(models.Model):

    _inherit = "res.partner"

    address2 = fields.Text(string="Địa chỉ 2")    
    address1 = fields.Text(readonly=True, string="Địa chỉ")    
    city_old = fields.Text()    

    @api.model
    def default_get(self, fields):
        # if self.env.context.get('default_opportunity_id'):
        #     self = self.with_context(
        #         default_res_model_id=self.env.ref('crm.model_crm_lead').id,
        #         default_res_id=self.env.context['default_opportunity_id']
        #     )
        defaults = super(ResPartner, self).default_get(fields)
        defaults['country_id'] = self.env.ref('base.vn').id
        # sync res_model / res_id to opportunity id (aka creating meeting from lead chatter)
        # if 'opportunity_id' not in defaults:
        #     if self._is_crm_lead(defaults, self.env.context):
        #         defaults['opportunity_id'] = defaults.get('res_id', False) or self.env.context.get('default_res_id', False)
        return defaults
    
    @api.onchange('street', 'city', 'state_id')
    def _onchange_city(self):
        alist = [self.street, self.city, self.state_id.name]
        alist = [i for i in alist if i]
        rs = ', '.join (alist)
        # origin = self.id.origin
        self.address1 = rs
