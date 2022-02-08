# from AptUrl.Helpers import _
from odoo import _
from odoo import fields, models, api
from datetime import datetime


class export_Indent(models.Model):
    _name = 'exportindent.data'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'customer_name'
    _order = "indent_no desc"

    @api.depends('export_bank_exp_line', 'export_bank_exp_line.expected_total_bank')
    def total_bank(self):
        for rec in self:
            total = 0
            for line in rec.export_bank_exp_line:
                total += line.expected_total_bank
            rec['total_bank_value'] = total

    @api.depends('export_bank_exp_line', 'export_bank_exp_line.actual_total_bank')
    def expo_actual_total_bank(self):
        for rec in self:
            total = 0
            for line in rec.export_bank_exp_line:
                total += line.actual_total_bank
            rec['total_bank_actual'] = total

    @api.depends('shipping_exp_line', 'shipping_exp_line.expected_total_shipping')
    def total_shipping(self):
        for rec in self:
            total = 0
            for line in rec.shipping_exp_line:
                total += line.expected_total_shipping
            rec['total_shipping_value'] = total

    @api.depends('shipping_exp_line', 'shipping_exp_line.actual_total_shipping')
    def expo_actual_total_shipping(self):
        for rec in self:
            total = 0
            for line in rec.shipping_exp_line:
                total += line.actual_total_shipping
            rec['total_shipping_actual'] = total

    @api.depends('expo_transportation_line', 'expo_transportation_line.expected_total_transportation')
    def total_transportation(self):
        for rec in self:
            total = 0
            for line in rec.expo_transportation_line:
                total += line.expected_total_transportation
            rec['total_transportation_value'] = total

    @api.depends('expo_transportation_line', 'expo_transportation_line.actual_total_transportation')
    def expo_actual_transportation(self):
        for rec in self:
            total = 0
            for line in rec.expo_transportation_line:
                total += line.actual_total_transportation
            rec['total_transportation_actual'] = total

    @api.depends('expo_cnf_line', 'expo_cnf_line.expected_total_cnf')
    def total_cnf(self):
        for rec in self:
            total = 0
            for line in rec.expo_cnf_line:
                total += line.expected_total_cnf
            rec['total_cnf_value'] = total

    @api.depends('expo_cnf_line', 'expo_cnf_line.actual_total_cnf')
    def expo_actual_total_cnf(self):
        for rec in self:
            total = 0
            for line in rec.expo_cnf_line:
                total += line.actual_total_cnf
            rec['total_cnf_actual'] = total

    @api.depends('expo_forwarder_line', 'expo_forwarder_line.expected_total_forwarder')
    def total_forwarder(self):
        for rec in self:
            total = 0
            for line in rec.expo_forwarder_line:
                total += line.expected_total_forwarder
            rec['total_forwarder_value'] = total

    @api.depends('expo_forwarder_line', 'expo_forwarder_line.actual_total_forwarder')
    def expo_actual_total_forwarder(self):
        for rec in self:
            total = 0
            for line in rec.expo_forwarder_line:
                total += line.actual_total_forwarder
            rec['total_forwarder_actual'] = total

    @api.depends('expo_courier_line', 'expo_courier_line.expected_total_courier')
    def total_courier(self):
        for rec in self:
            total = 0
            for line in rec.expo_courier_line:
                total += line.expected_total_courier
            rec['total_courier_value'] = total

    @api.depends('expo_courier_line', 'expo_courier_line.actual_total_courier')
    def expo_actual_total_courier(self):
        for rec in self:
            total = 0
            for line in rec.expo_courier_line:
                total += line.actual_total_courier
            rec['total_courier_actual'] = total

    ########################## Here calculate Final value############################
    @api.depends('total_bank_value', 'total_bank_actual')
    def final_bank_count(self):
        for rec in self:
            rec.final_bank_exp = rec.total_bank_value - rec.total_bank_actual

    @api.depends('total_shipping_value', 'total_shipping_actual')
    def final_shipping_count(self):
        for rec in self:
            rec.final_shipping = rec.total_shipping_value - rec.total_shipping_actual

    @api.depends('total_transportation_value', 'total_transportation_actual')
    def final_transportation_count(self):
        for rec in self:
            rec.final_transportation = rec.total_transportation_value - rec.total_transportation_actual

    @api.depends('total_cnf_value', 'total_cnf_actual')
    def final_cnf_count(self):
        for rec in self:
            rec.final_cnf= rec.total_cnf_value - rec.total_cnf_actual

    @api.depends('total_forwarder_value', 'total_forwarder_actual')
    def final_forwarder_count(self):
        for rec in self:
            rec.final_forwarder= rec.total_forwarder_value - rec.total_forwarder_actual

    @api.depends('total_courier_value', 'total_courier_actual')
    def final_courier_count(self):
        for rec in self:
            rec.final_courier= rec.total_courier_value - rec.total_courier_actual

    customer_name = fields.Char(string="Customer Name", required=True)
    po_no = fields.Integer(string="P.O no", required=True, )
    pi_no = fields.Integer(string="P.I no", required=True, )
    total_invoice_value = fields.Integer(string="Total Invoice Value", required=True, )
    ship_terms = fields.Selection(string="Shipping Terms", selection=[('fob', 'FOB'), ('cnf', 'CNF'), ],
                                  required=True, )
    ship_by = fields.Selection(string="Shipping By", selection=[('air', 'AIR'), ('sea', 'SEA'), ], required=True, )
    indent_no = fields.Char(string='Indent No', required=True, copy=False, readonly=True, index=True,
                            default=lambda self: _('New'))
    indent_date = fields.Datetime(string="Indent Date", default=datetime.today(), readonly="1")
    export_bank_exp_line = fields.One2many(comodel_name="exportbank.expense", inverse_name="expo_bank_expense_line",
                                           string="Import Bank Expense")
    shipping_exp_line = fields.One2many(comodel_name="shippingdocument.expense", inverse_name="shipping_expense_line",
                                        string="Import Doc Expense")
    expo_transportation_line = fields.One2many(comodel_name="exporttransportation.cost",
                                               inverse_name="expo_transportation_cost_line",
                                               string="Transportation cost Line")
    expo_cnf_line = fields.One2many(comodel_name="exportcnf.cost", inverse_name="expo_cnf_cost_line",
                                    string="Cnf cost Line")
    expo_forwarder_line = fields.One2many(comodel_name="exportforwarder.cost", inverse_name="expo_forwarder_cost_line",
                                          string="Forwarder cost Line")
    expo_courier_line = fields.One2many(comodel_name="exportcourier.cost", inverse_name="expo_courier_cost_line",
                                        string="Courier cost Line")

    total_bank_value = fields.Float(string="Total", compute='total_bank', store=True)
    total_shipping_value = fields.Float(string="Total", compute='total_shipping', store=True)
    total_transportation_value = fields.Float(string="Total", compute='total_transportation', store=True)
    total_cnf_value = fields.Float(string="Total", compute='total_cnf', store=True)
    total_forwarder_value = fields.Float(string="Total", compute='total_forwarder', store=True)
    total_courier_value = fields.Float(string="Total", compute='total_courier', store=True)

    total_bank_actual = fields.Float(string="Total", compute='expo_actual_total_bank', store=True)
    total_shipping_actual = fields.Float(string="Total", compute='expo_actual_total_shipping', store=True)
    total_transportation_actual = fields.Float(string="Total", compute='expo_actual_transportation', store=True)
    total_cnf_actual = fields.Float(string="Total", compute='expo_actual_total_cnf', store=True)
    total_forwarder_actual = fields.Float(string="Total", compute='expo_actual_total_forwarder', store=True)
    total_courier_actual = fields.Float(string="Total", compute='expo_actual_total_courier', store=True)


    ###################For final calculation#####################

    final_bank_exp = fields.Float(string="Final Amount", compute='final_bank_count', store=True)
    final_shipping = fields.Float(string="Final Amount", compute='final_shipping_count', store=True)
    final_transportation = fields.Float(string=" Final Amount", compute='final_transportation_count',
                                        store=True)
    final_cnf = fields.Float(string="Final Amount", compute='final_cnf_count', store=True)
    final_forwarder = fields.Float(string="Final Amount", compute='final_forwarder_count', store=True)
    final_courier = fields.Float(string="Final Amount", compute='final_courier_count', store=True)

    @api.model
    def create(self, vals):
        if vals.get('indent_no', _('New')) == _('New'):
            vals['indent_no'] = self.env['ir.sequence'].next_by_code('export.indent.seq') or _('New')
        result = super(export_Indent, self).create(vals)
        return result


class Export_bank_expense(models.Model):
    _name = 'exportbank.expense'
    _description = "Bank Expenses Line"

    # export_bank_expense = fields.Selection(string="", selection=[('conveyance', 'Conveyance'),
    #                                                              ('entertainment', 'Entertainment'), ('print', 'Print'),
    #                                                              ('bank_charge_postage', 'Bank Charge Postage'),
    #                                                              ('bank_charge_commission', 'Bank Charge Commission'),
    #                                                              ('bank_vat_commission',
    #                                                               'Bank Charge VAT on Commission'),
    #                                                              ('source_tax_ait', 'Source Tax AIT'),
    #                                                              ], required=True, )
    export_bank_expense = fields.Many2one(comodel_name="expdynamic.field", string="Export Bank Expense", required=True, )
    expo_bank = fields.Float(related='export_bank_expense.conf_expo_bank', string="Bank",)
    expo_cash = fields.Float(related='export_bank_expense.conf_expo_cash', string="Cash",)
    actual_expo_bank = fields.Float(string="Actual Bank")
    actual_expo_cash = fields.Float(string="Actual Cash")
    expo_remarks = fields.Text(string="Remarks")
    actual_total_bank = fields.Float(string="Actual Total", compute='count_bank_actual_total', store=True)
    expected_total_bank = fields.Float(string="Expected Total", compute='count_bank_expected_total', store=True)
    expo_bank_expense_line = fields.Many2one('exportindent.data', string="Export Bank Expense Line Id")

    @api.depends('expo_bank', 'expo_cash')
    def count_bank_expected_total(self):
        for total in self:
            total.expected_total_bank = total.expo_bank + total.expo_cash

    @api.depends('actual_expo_bank', 'actual_expo_cash')
    def count_bank_actual_total(self):
        for total in self:
            total.actual_total_bank = total.actual_expo_bank + total.actual_expo_cash


class Shipping_document_expense(models.Model):
    _name = 'shippingdocument.expense'
    _description = "Import Document expense Line"

    # shipping_doc_exp = fields.Selection(string="Shipping document Expense",
    #                                     selection=[('gsp_co_purchase', 'GSP CO Purchase'),
    #                                                ('gsp_endorsement', 'GSP Endorsement'), (
    #                                                    'gsp_issue',
    #                                                    'GSP Issue Misc'),
    #                                                ('conveyance', 'Conveyance'),
    #                                                ('entertainment', 'Entertainment'),
    #                                                ('print', 'Print Or Photocopy'),
    #                                                ('export_certificate', 'Export Certificate'),
    #                                                ('stamp', 'Stamp')], required=True, )
    shipping_doc_exp = fields.Many2one(comodel_name="dynamic.expdocuments", string="Shipping document Expense", required=True, )
    shipping_bank = fields.Float(related='shipping_doc_exp.conf_shipping_bank', string="Bank", required=False, )
    shipping_cash = fields.Float(related='shipping_doc_exp.conf_shipping_cash', string="Cash", required=False, )

    actual_shipping_bank = fields.Float(string="Actual Bank")
    actual_shipping_cash = fields.Float(string="Actual Cash")
    shipping_remarks = fields.Text(string="Remarks")
    actual_total_shipping = fields.Float(string="Actual Total", compute='count_shipping_actual_total', store=True)
    expected_total_shipping = fields.Float(string="Expected Total", compute='count_shipping_expected_total', store=True)
    shipping_expense_line = fields.Many2one('exportindent.data', string="shipping Expense Line Id")

    @api.depends('shipping_bank', 'shipping_cash')
    def count_shipping_expected_total(self):
        for total in self:
            total.expected_total_shipping = total.shipping_bank + total.shipping_cash

    @api.depends('actual_shipping_bank', 'actual_shipping_cash')
    def count_shipping_actual_total(self):
        for total in self:
            total.actual_total_shipping = total.actual_shipping_bank + total.actual_shipping_cash


class Export_transportation_cost(models.Model):
    _name = 'exporttransportation.cost'
    _description = "Transportation Cost Line"

    # expo_transportation_cost = fields.Selection(string="Transportation Cost",
    #                                             selection=[('carriage_inwards', 'Carriage Inwards'),
    #                                                        ('parking_fee', 'toll or Parking fees'), ], required=True, )
    expo_transportation_cost = fields.Many2one(comodel_name="dynamic.exptransportation", string="Transportation Cost", required=True, )
    expo_transport_bank = fields.Float(related='expo_transportation_cost.conf_expo_transport_bank', string="Bank")
    expo_transport_cash = fields.Float(related='expo_transportation_cost.conf_expo_transport_cash', string="Cash")

    actual_trans_bank = fields.Float(string="Actual Bank")
    actual_trans_cash = fields.Float(string="Actual Cash")
    expo_transportation_remarks = fields.Text(string="Remarks")
    actual_total_transportation = fields.Float(string="Actual Total", compute='count_transportation_actual_total',
                                               store=True)
    expected_total_transportation = fields.Float(string="Expected Total", compute='count_transportation_expected_total',
                                                 store=True)
    expo_transportation_cost_line = fields.Many2one('exportindent.data', string="transportation Line Id")

    @api.depends('expo_transport_bank', 'expo_transport_cash')
    def count_transportation_expected_total(self):
        for total in self:
            total.expected_total_transportation = total.expo_transport_bank + total.expo_transport_cash

    @api.depends('actual_trans_bank', 'actual_trans_cash')
    def count_transportation_actual_total(self):
        for total in self:
            total.actual_total_transportation = total.actual_trans_bank + total.actual_trans_cash


class Export_cnf_cost(models.Model):
    _name = 'exportcnf.cost'
    _description = "Export C & F cost line"

    # expo_cnf_cost = fields.Selection(string="C & f Cost", selection=[('cf_bill', 'C & f Bill')], required=True, )
    expo_cnf_cost = fields.Many2one(comodel_name="dynamic.expcnf", string="C & f Cost", required=True, )
    expo_cnf_bank = fields.Float(related='expo_cnf_cost.conf_expo_cnf_bank', string="Bank")
    expo_cnf_cash = fields.Float(related='expo_cnf_cost.conf_expo_cnf_cash', string="Cash")
    actual_expo_cnf_bank = fields.Float(string="Actual Bank")
    actual_expo_cnf_cash = fields.Float(string="Actual Cash")
    expo_cnf_remarks = fields.Text(string="Remarks")
    actual_total_cnf = fields.Float(string="Actual Total", compute='count_cnf_expected_total', store=True)
    expected_total_cnf = fields.Float(string="Expected Total", compute='count_cnf_expected_total', store=True)
    expo_cnf_cost_line = fields.Many2one('exportindent.data', string="cnf Line Id")

    @api.depends('expo_cnf_bank', 'expo_cnf_cash')
    def count_cnf_expected_total(self):
        for total in self:
            total.expected_total_cnf = total.expo_cnf_bank + total.expo_cnf_cash

    @api.depends('actual_expo_cnf_bank', 'actual_expo_cnf_cash')
    def count_cnf_actual_total(self):
        for total in self:
            total.actual_total_cnf = total.actual_expo_cnf_bank + total.actual_expo_cnf_cash


class Export_forwarder_cost(models.Model):
    _name = 'exportforwarder.cost'
    _description = "Forwarder cost line"
    #
    # expo_forwarder_cost = fields.Selection(string="Forwarder Cost", selection=[('forwarder_bill', 'Forwarder Bill')],
    #                                        required=True, )
    expo_forwarder_cost = fields.Many2one(comodel_name="dynamic.expforwarder", string="Forwarder Cost", required=True, )
    expo_forwarder_bank = fields.Float(related='expo_forwarder_cost.conf_expo_forwarder_bank', string="Bank")
    expo_forwarder_cash = fields.Float(related='expo_forwarder_cost.conf_expo_forwarder_cash', string="Cash")

    actual_expo_forwarder_bank = fields.Float(string="Actual Bank")
    actual_expo_forwarder_cash = fields.Float(string="Actual Cash")
    expo_forwarder_remarks = fields.Text(string="Remarks")
    actual_total_forwarder = fields.Float(string="Actual Total", compute='count_forwarder_actual_total',
                                          store=True)
    expected_total_forwarder = fields.Float(string="Expected Total", compute='count_forwarder_expected_total',
                                            store=True)
    expo_forwarder_cost_line = fields.Many2one('exportindent.data', string="Forwarder Line Id")

    @api.depends('expo_forwarder_bank', 'expo_forwarder_cash')
    def count_forwarder_expected_total(self):
        for total in self:
            total.expected_total_forwarder = total.expo_forwarder_bank + total.expo_forwarder_cash

    @api.depends('actual_expo_forwarder_bank', 'actual_expo_forwarder_cash')
    def count_forwarder_actual_total(self):
        for total in self:
            total.actual_total_forwarder = total.actual_expo_forwarder_bank + total.actual_expo_forwarder_cash


class Export_courier_charge(models.Model):
    _name = 'exportcourier.cost'
    _description = "Courier Charge line"

    # expo_courier_charge = fields.Selection(string="Courier Charge", selection=[('courier_bill', 'Courier Bill')],
    #                                        required=True, )
    expo_courier_charge = fields.Many2one(comodel_name="dynamic.expcourier", string="Courier Charge", required=True, )
    expo_courier_bank = fields.Float(related='expo_courier_charge.conf_expo_courier_bank', string="Bank")
    expo_courier_cash = fields.Float(related='expo_courier_charge.conf_expo_courier_cash', string="Cash")

    actual_expo_courier_bank = fields.Float(string="Actual Bank")
    actual_expo_courier_cash = fields.Float(string="Actual Cash")
    expo_courier_remarks = fields.Text(string="Remarks")
    actual_total_courier = fields.Float(string="Actual Total", compute='count_courier_actual_total', store=True)
    expected_total_courier = fields.Float(string="Expected Total", compute='count_courier_expected_total', store=True)
    expo_courier_cost_line = fields.Many2one('exportindent.data', string="Courier Line Id")

    @api.depends('expo_courier_bank', 'expo_courier_cash')
    def count_courier_expected_total(self):
        for total in self:
            total.expected_total_courier = total.expo_courier_bank + total.expo_courier_cash

    @api.depends('actual_expo_courier_bank', 'actual_expo_courier_cash')
    def count_courier_actual_total(self):
        for total in self:
            total.actual_total_courier = total.actual_expo_courier_bank + total.actual_expo_courier_cash
