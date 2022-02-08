from odoo import api, fields, models, _
# from datetime import datetime


class ProductDetails(models.Model):
	_name = 'product.data'
	
	product_name = fields.Char(string="Product Name", required=True)
	product_price = fields.Char(string="Product Price", required=True)
	product_quantity = fields.Char(string="Product Quantity", required=True)
