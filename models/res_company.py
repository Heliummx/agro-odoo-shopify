from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    shopify_product_upload_url = fields.Char(string="Shopify product upload url")
