# -*- coding: utf-8 -*-
{
    'name': 'Aeroo Reports - TLTEK',
    'category': 'Tools',
    'summary': 'Enterprise level reporting solution developed by Numigi and migrated by TLTEK.',
    'author': 'TLTEK',
    # 'author_email': 'Kim Duong <kim.duong986@gmail.com>',
    'depends': ['mail'],
    # 'external_dependencies': {
    #     'python': ['aeroolib', 'babel', 'genshi'],
    # },
    # 'excludes': [
    #     'report_aeroo',
    # ],
    'data': [
        "data/report_aeroo_data.xml",
        
        "security/ir.model.access.csv",
        
        "views/ir_actions_report.xml",
        "views/mail_template.xml",
        
        "demo/report_sample.xml",
    ],
    'assets':{
        'web.assets_backend':['report_aeroo_tltek/static/src/js/action_manager.js',],
     },
    # 'installable': True,
    # 'application': True,
    # 'license': 'GPL-3 or any later version'
}
