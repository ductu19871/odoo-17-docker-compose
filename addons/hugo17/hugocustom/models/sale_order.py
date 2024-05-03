from odoo import api, fields, models

class SO(models.Model):
    _inherit = 'sale.order'

    quotation_term = fields.Integer(default=7)#'Hiệu lực báo giá', 
    add_state = fields.Selection([('send_request','Đã gửi yêu cầu xử lý'),
                                  ('confirmed', 'Xác nhận đơn hàng'),
                                  ('stocked', 'Đã xuất kho'),
                                  ('setup','Đang lắp đặt'),
                                  ('deliveried','Giao hàng thành công'),
                                  ('closed','Đơn hàng đã đóng'),
                                  ], string='Sale order state')#'Các trạng thái của đơn hàng'
    payment_method_id = fields.Many2one('account.payment.method', domain="[('payment_type','=','inbound')]")#'Phương thức thanh toán',
    advance_money = fields.Monetary(currency_field='currency_id')#Tiền cọc
    delivery_method_id = fields.Many2one('sale.delivery.method')
    note2 = fields.Text()
    ckt = fields.Integer(default=100, string='Chuyển khoản trước')
    delivery_interval = fields.Char(default='05~07', string='Giao hàng trong vòng')
    def _prepare_invoice(self):
        return super(SO, self.with_context(overwrite_user_warehouse_id = self.warehouse_id ))._prepare_invoice()
    
    def gen_dktt(self):#điều kiện thanh toán
        if self.ckt == 100:
            return f'Chuyển khoản {self.ckt}% khi đặt hàng'
        elif self.ckt:
            return f'Chuyển khoản {self.ckt}% khi đặt hàng, phần còn lại sẽ thanh toán khi có thông báo giao hàng'
        else:
            return 'Thanh toán khi có thông báo giao hàng'

