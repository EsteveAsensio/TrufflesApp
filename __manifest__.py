# -*- coding: utf-8 -*-
{
 'name': "trufflesapp",

    'summary': """
        Control the statistics of Truffle""",

    'description': """
    """,

    'author': "Esteve Asensio",
    'website': "https://www.trufflesesteve.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/weight.xml',
        'views/quality.xml',
        'views/product.xml',
        'views/invoice.xml',
        'views/invoicelines.xml',
        'views/category.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
}
