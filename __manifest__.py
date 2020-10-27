{
    'name': 'Shopify product upload',
    'version': '1.0',
    'summary': 'upload your products to shopify',
    'description': 'This module will add the feature of uploading the product and all '
                   'its variants using action server, if the upload is successful, it will'
                   'return the shopify id of the product',
    'category': 'Inventory, Logistic, Storage',
    'author': '',
    'website': '',
    'license': '',
    'depends': ['base', 'product', 'stock'],
    'data': ['views/product.xml',
             'views/res_company.xml'],
    'installable': True,
    'auto_install': False,

}
