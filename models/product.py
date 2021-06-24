from odoo import models, fields, api, _
import requests
import json
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    shopify_product_id = fields.Char()
    shopify_handle = fields.Char(string="Shopify Handle")

    def get_product_spareparts(self):
        spare_products = [];
        for product in self.spare_parts_product_ids:
            spare_products.append({
                "sku": product.default_code,
                "shopify_id": product.shopify_product_id,
                "shopify_handle":product.shopify_handle
            })
        return spare_products

    def get_alternatives_products(self):
        alt_products = []
        for alt_product in self.alternative_product_ids:
            alt_products.append({
                "sku": alt_product.default_code,
                "shopify_id": alt_product.shopify_product_id,
                "shopify_handle":alt_product.shopify_handle
            })
        return alt_products

    def get_products_accesories(self):
        acc_products = []
        for acc_product in self.accessory_product_ids:
            acc_products.append({
                "sku": acc_product.default_code,
                "shopify_id": acc_product.shopify_product_id,
                "shopify_handle":acc_product.shopify_handle
            })
        return acc_products


    def get_product_parent_tags(self):
        res_categ = []
        for categs in self.public_categ_ids:
            current_category = categs;
            while current_category:
                pair_split = {
                    "parent_tag": current_category.parent_id.name,
                    "son_tag": current_category.name
                }
                current_category = current_category.parent_id
                res_categ.append(pair_split)
            ## res_categ.append(categs.display_name.split('/'))
        # if res_categ:
        #     if len(res_categ) <= 1:
        #         res_categ = res_categ[0]

        return res_categ

    def get_shopify_data_upload(self):
        _logger.info(_("Started getting data of the product %s") % self.name)
        variants = self.product_variant_ids
        product_image = ''
        table_image = ''
        additional_images = []
        taxes_amounts = []
        if self.image:
            product_image = self.image.decode('utf-8')
        if self.x_studio_image_shopify:
            table_image = self.x_studio_image_shopify.decode('utf-8')
        for image_data in self.product_image_ids:
            additional_images.append( image_data.image.decode('utf-8') )
        if self.taxes_id:
            for tax in self.taxes_id:
                taxes_amounts.append(tax.amount)
        shopify_data_post = {
            "title": self.name,
            "vendor": self.product_brand_id.mapped('display_name'), # Revisar en que campo está el nombre.
            "shopify_product_id": self.shopify_product_id,
            "description": self.website_description,
            "tags": self.get_product_parent_tags(),
            "images": product_image,
            "table_image": table_image,
            "additional_images": additional_images,
            "is_published": self.x_studio_website_shopify,
            "product_accesories": self.get_products_accesories(),
            "product_alternatives": self.get_alternatives_products(),
            "spare_products": self.get_product_spareparts(),
            "taxes":taxes_amounts,
            "variants": [
                {
                    "sku": variant.default_code,
                    "variant_data": [{variant_attribute.attribute_id.display_name: variant_attribute.name} for
                                     variant_attribute in
                                     variant.attribute_value_ids],

                    "stock": variant.qty_available_not_res,
                    "sales_price": variant.list_price,
                    "barcode": variant.barcode,
                    "taxable": bool(variant.taxes_id),
                    "shopify_variant_id": variant.shopify_variant_id,
                    "inventory_item_id": variant.shopify_inventory_item_id
                } for variant in variants
            ]
        }
        return shopify_data_post

    def upload_product_to_shopify(self):
        for line in self:
            upload_data = line.get_shopify_data_upload()
            if upload_data:
                headers = {'Content-Type': 'application/json'}
                data_json = json.dumps({'params': upload_data})

                try:
                    shopify_product_upload_url = self.env.user.company_id.shopify_product_upload_url
                    requests.post(url=shopify_product_upload_url, data=data_json, headers=headers)
                except Exception as e:
                    _logger.error(
                        "Failed to send post request to shopify for upload the product %s, reason : %s" % (
                            self.name, e))
            else:
                _logger.error(_("The upload data is empty for the product %s") % (self.name))


class ProductProduct(models.Model):
    _inherit = 'product.product'

    shopify_variant_id = fields.Char(string="Shopify variant_id")
    shopify_inventory_item_id = fields.Char(string="Shopify inventory_item_id")
