
{
    "name": "Hugo custom",
    "summary": "Hugo custom"
    "company",
    "version": "17.0.1.0.6",
    "author": "NDT ",
    "website": "",
    "category": "Generic",
    "depends": ['sale','purchase', 'stock', 'account', 'report_aeroo_tltek','hugobase'],
    "license": "LGPL-3",
    "data": [
        "data/account.account.csv",
        "data/account.journal.csv",
        # "data/account.payment.method.line.csv",
        "security/ir.model.access.csv",
        # "security/ir_rule.xml",
        "data/stock_data.xml",
        # "data/account_data.xml",
        "data/sale_delivery_method_data.xml",
        "data/account_payment_method.xml",
        "view/res_users_view.xml",
        "view/res_partner_view.xml",
        "view/sale_order_view.xml",
        "view/report.xml",
        "view/sale_delivery_method.xml",
    ],
    # "installable": True,
}
