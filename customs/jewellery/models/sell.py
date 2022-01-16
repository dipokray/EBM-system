from odoo import fields, models, api
from datetime import datetime


class SellProduct(models.Model):
    _name = 'sell.product'
    _rec_name = 'product_seq'

    # def product(self):
    #     name = self.env['product.create'].search([])
    #     print(name)

    product_seq = fields.Many2one(comodel_name="product.create", string="Product ID", required=False, )
    product_name = fields.Char(related='product_seq.product_name', string="Product Name", required=False, )
    product_image = fields.Binary(related='product_seq.product_image', string=" Image", required=False, )
    gold_quality = fields.Selection(related='product_seq.gold_quality', string="Gold Quality", required=False, )
    gold_rate = fields.Integer(related='product_seq.gold_rate', string="Gold Rate", required=False, )
    gold_weight = fields.Float(related='product_seq.gold_weight', string="Gold Weight", required=False, )
    making_cost = fields.Integer(related='product_seq.making_cost', string="Making Cost", required=False, )
    tax = fields.Integer(related='product_seq.tax', string="Tax", required=False, )
    gold_price = fields.Integer(related='product_seq.total_cost', string="Total Price",
                                required=False, )
    sell_product_quantity = fields.Integer(string="Product Quantity", required=True, )
    gold_price_new = fields.Integer(string="Total Price", compute='compute_price', store=True, )

    payment = fields.Integer(string="Payment")
    due_amount = fields.Integer(string="Due", compute='due_compute', store=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company.id)
    currency_id = fields.Many2one("res.currency", string="Currency", readonly=True,
                                  default=lambda self: self.env.company.currency_id.id, required=True)

    # sell_line = fields.Many2one(comodel_name="product.create", string="Sell Line", required=False, )

    @api.model
    def create(self, vals):
        res = super(SellProduct, self).create(vals)
        remain_qty = res.product_seq.product_quantity - res.sell_product_quantity
        res.product_seq.product_quantity = remain_qty
        return res

    @api.depends('gold_price', 'sell_product_quantity')
    def compute_price(self):
        for rec in self:
            rec.gold_price_new = rec.gold_price * rec.sell_product_quantity

    @api.depends('gold_price_new','payment')
    def due_compute(self):
        for rec in self:
            rec.due_amount = rec.gold_price_new - rec.payment
