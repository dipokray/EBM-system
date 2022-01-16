from odoo import fields, models, api
from datetime import datetime
from AptUrl.Helpers import _


class Order(models.Model):
    _name = 'order.order'
    _inherit = ['mail.thread', 'mail.activity.mixin', ]
    _description = "Order Receive Data"
    _rec_name = 'customer_name'

    @api.depends('gold_orderline', 'gold_orderline.sub_total_price')
    def sum_sub_total(self):
        for rec in self:
            total = 0
            for line in rec.gold_orderline:
                total += line.sub_total_price
            rec['sum_of_sub_total'] = total

    @api.depends('paymentline', 'paymentline.pay_amount')
    def sum_pay_total(self):
        for rec in self:
            total = 0
            for line in rec.paymentline:
                total += line.pay_amount
            rec['sum_of_pay_total'] = total

    @api.depends('sum_of_sub_total', 'sum_of_pay_total')
    def total_due(self):
        for rec in self:
            rec.due = rec.sum_of_sub_total - rec.sum_of_pay_total

    sum_of_sub_total = fields.Monetary(string="Total Price", compute="sum_sub_total", store=True)
    sum_of_pay_total = fields.Monetary(string="Total Payment", compute="sum_pay_total", store=True)
    due = fields.Integer(string="Total Due", compute="total_due", store=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company.id)
    currency_id = fields.Many2one("res.currency", string="Currency", readonly=True,
                                  default=lambda self: self.env.company.currency_id.id, required=True)
    # default = lambda self: self.env.company.currency_id.id,

    order_status = fields.Boolean(string="Ready Product")
    order_seq = fields.Char(string='OID', required=True, copy=False,
                            randomly=True, index=True,readonly=True,
                            default=lambda self: _('New'))
    customer_name = fields.Char(string="Name", required=False)
    customer_mob = fields.Integer(string="Mobile No.", required=True)
    customer_address = fields.Char(string="Address", required=False, )
    product_type = fields.Selection(string="Product Type", selection=[('gold', 'Gold'), ('silver', 'Silver'), ],
                                    required=False, )
    # gold_rate = fields.Integer(string="Gold Rate", required=True, )
    order_date = fields.Datetime(string="Date", default=fields.datetime.now(), readonly="1")
    dele_date = fields.Datetime(string="Delivery Date", required=True)
    gold_orderline = fields.One2many(comodel_name="orderline.data", inverse_name="create_orderline",
                                     string="gold order", )
    paymentline = fields.One2many(comodel_name="paymentline.data", inverse_name="create_paymentline",
                                  string="gold payment", )

    @api.model
    def create(self, vals):
        if vals.get('order_seq', _('New')) == _('New'):
            vals['order_seq'] = self.env['ir.sequence'].next_by_code('order.data.sequence') or _('New')
        result = super(Order, self).create(vals)
        return result


class Order_Line(models.Model):
    _name = 'orderline.data'
    _description = "Oder details"

    product_name = fields.Selection(string="Product Name",
                                    selection=[('chain', 'Chain'), ('nackless', 'Nackless'), ('har', 'Har'),
                                               ('churi', 'Churi'), ('yearring', 'Year-Ring')], required=True, )
    weight = fields.Float(string="Weight", required=True)
    product_image = fields.Binary(string="Image")
    product_quantity = fields.Integer(string="Quantity", required=True)
    making_cost = fields.Integer(string="Making cost", )
    gold_rate = fields.Float(string="Gold Rate", required=True, )
    sub_total_price = fields.Float(string="Sub Total Price", compute='gold_cost_count', store=True)
    create_orderline = fields.Many2one('order.order', string="Oder Line")

    @api.depends('weight', 'gold_rate')
    def gold_cost_count(self):
        for rec in self:
            rec.sub_total_price = ((rec.gold_rate / 96 * rec.weight) + rec.making_cost)


class PaymentLine(models.Model):
    _name = 'paymentline.data'
    # _inherits = {'orderline.data': 'sub_total_price'}
    _description = "Payment Details"

    current_date = fields.Datetime(string="Date", default=datetime.today(), readonly=True, )
    pay_amount = fields.Integer(string="Payment")
    create_paymentline = fields.Many2one('order.order', string="Payment Line")

    # def create(self, vals):
    #     id = 0
    #     rec = super(PaymentLine, self).create(vals)
    #     if not vals['price_id']:
    #         new_value = {'product_quantity': vals['product_quantity']}
    #         rec['price_id'] = self.env['orderline.data'].create(new_value).id
    #     print('value chnage', vals['price_id'], id, rec)
    #     return rec
