from odoo import api, fields, models, tools, _


class Lang(models.Model):
    _inherit = "res.lang"

    @api.model
    # def active_a_lang(self, lang='vi_VN'):
    def active_a_lang(self, lang):
        # langs = self.search([('code','=',lang)])
        langs_test = self.env['res.lang'].search([])
        langs = self.env['res.lang'].with_context(active_test=False).search([('code','=',lang)])
        wz = self.env['base.language.install'].create({'lang_ids': [(6,0,langs.ids)]})
        wz.lang_install()
        