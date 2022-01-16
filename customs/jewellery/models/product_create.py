from AptUrl.Helpers import _

from odoo import fields, models, api
from datetime import datetime


class ProductCreate(models.Model):
    _name = 'product.create'
    _inherit = ['mail.thread', 'mail.activity.mixin', ]
    _rec_name = 'product_seq'

    product_seq = fields.Char(string='PID', required=True, copy=False,
                              randomly=True, index=True,
                              default=lambda self: _('New'))
    product_name = fields.Char(string="Product Name")
    product_image = fields.Binary(string="Product Image")
    product_quantity = fields.Integer(string="Product Quantity", )
    gold_quality = fields.Selection(string="Gold Quality", selection=[('18k', '18K'), ('21k', '21K'), ('22k', '22K')],
                                    required=True, )
    gold_rate = fields.Integer(string="Gold Rate")
    gold_weight = fields.Float(string="Weight/Gram", required=True)
    making_cost = fields.Integer(string="Making Cost")
    gold_price = fields.Integer(string="Sub-total Price", compute='compute_sub_total_price', store=True)
    tax = fields.Integer(string="Tax", )
    tax_cal = fields.Integer(string="tax Calculation", compute='compute_tax', store=True)
    total_cost = fields.Integer(string="Total Price", compute='compute_total_price', store=True)

    # create_sell_line = fields.One2many(comodel_name="sell.product", inverse_name="sell_line", string="create sell line",
    #                                    required=False, )
    # product_quantity_new = fields.Integer()
    # refer_product = fields.Many2one('sell.product', string="Refer product")

    @api.depends('gold_rate', 'gold_weight', 'making_cost')
    def compute_sub_total_price(self):
        for rec in self:
            rec.gold_price = rec.gold_rate * rec.gold_weight + rec.making_cost

    @api.depends('gold_price')
    def compute_tax(self):
        for rec in self:
            rec.tax_cal = (rec.gold_price * rec.tax) / 100

    @api.depends('gold_price', 'tax_cal')
    def compute_total_price(self):
        for rec in self:
            rec.total_cost = rec.gold_price + rec.tax_cal

    @api.model
    def create(self, vals):
        if vals.get('product_seq', _('New')) == _('New'):
            vals['product_seq'] = self.env['ir.sequence'].next_by_code('product.data.sequence') or _('New')
        result = super(ProductCreate, self).create(vals)
        return result


class WeightConfig(models.Model):
    _name = 'weight.config'

    weight_type = fields.Selection(string="Weight Type", selection=[('roti', 'Roti'), ('gram', 'Gram')],
                                   required=True, default='gram')
