# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.tools.misc import get_lang
import re
from bs4 import BeautifulSoup

class Base(models.AbstractModel):
    _inherit = 'base'
    
    def format_number(self, amount, decimal_places=0, lang_code=False, env=None):

        if not env:
            env = self.env
        if isinstance(decimal_places, str):
            decimal_places = env['decimal.precision'].precision_get(decimal_places)
        fmt = "%.{0}f".format(decimal_places)
        lang = get_lang(env, lang_code)

        formatted_amount = lang.format(fmt, amount, grouping=True, monetary=True)\
            .replace(r' ', u'\N{NO-BREAK SPACE}').replace(r'-', u'-\N{ZERO WIDTH NO-BREAK SPACE}')
        return formatted_amount
    
    
    
    def format_amount_wo_symbol(self, amount, currency=None, lang_code=False, env=None):
        if not currency:
            currency = self.currency_id or self.env['res.currency'].search([('name','=', 'VND')])
        if not env:
            env = self.env
        fmt = "%.{0}f".format(currency.decimal_places)
        lang = get_lang(env, lang_code)

        formatted_amount = lang.format(fmt, currency.round(amount), grouping=True, monetary=True)\
            .replace(r' ', u'\N{NO-BREAK SPACE}').replace(r'-', u'-\N{ZERO WIDTH NO-BREAK SPACE}')
        return formatted_amount

    def format_amount_wo_symbol_vi(self, amount, currency=None, env=None, swap_punctuation=True):
        rs = self.format_amount_wo_symbol(amount, currency=currency, lang_code='vi_VN', env=env)
        if swap_punctuation:
            rs = rs.split('.')
            rs[-1] = rs[-1].replace(',', '.')
            rs = ','.join(rs)
        return rs

    def replace_multiple_newline(self, input_string, repl=', '):
        if input_string.isspace():
            return ''
        return re.sub(pattern=r'\n+', repl=repl, string=input_string)
    
    def num2words_eq_vi(self, amount):
        return self.env['to.vietnamese.number2words'].num2words(amount, precision_digits=0) + ' đồng chẵn'

    def format_ngay_thang_nam(self, dt):
        return dt.strftime("ngày %d tháng %m năm %Y")
        
    def format_ngay_thang_nam_today(self):
        today = fields.Date.context_today(self)
        return self.format_ngay_thang_nam(today)
        
    def aeroo_convert_html(self, html_string):
        if not html_string:
            return ''
        soup = BeautifulSoup(html_string, 'html.parser')
        content = soup.get_text(separator=',', strip=True)
        return content
