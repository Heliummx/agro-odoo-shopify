{
    'name': 'Shopify odoo inventory synchronisation',
    'version': '1.0',
    'summary': 'Synchronise sales and qty of product of odoo and shopify',
    'description': 'This module will synchronise the sale order creation of odoo and shopify as well as the qtys ajustments',
    'category': 'sale',
    'author': '',
    'website': '',
    'license': '',
    'depends': ['base', 'sale', 'sale_management', 'stock'],
    'data': [
        'views/res_partner.xml',
        'views/res_company.xml',
    ],
    'installable': True,
    'auto_install': False,

}
