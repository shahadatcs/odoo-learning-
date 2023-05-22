# -*- coding: utf-8 -*-
{
    'name': "om_odoo_inheritence",
    'summary': """""",
    'description': """""",
    'sequence': -99,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['sale', 'sale_stock', 'mail'],
    'data': [
        'views/sale_order_view.xml',
        'views/account_move_view.xml',
        'views/res_partner_category_view.xml',
    ],
    'demo': [],
}
