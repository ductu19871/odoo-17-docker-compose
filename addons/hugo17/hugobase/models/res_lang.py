from odoo import api, fields, models, tools, _


class Lang(models.Model):
    _inherit = "res.lang"

    @api.model
    def active_a_lang(self, lang='vi_VN'):
        langs = self.search([('code','=',lang)])
        wz = self.env['base.language.install'].create({'lang_ids': [(6,0,langs.ids)]})
        wz.lang_install()
        