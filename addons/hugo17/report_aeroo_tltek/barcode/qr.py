# -*- coding: utf-8 -*-
def make_qr_code(code):
    import qrcode

    qr = qrcode.QRCode(box_size=10)
    qr.add_data(code)
    qr.make(fit=True)

    return qr.make_image(fill_color="black", back_color="white")
