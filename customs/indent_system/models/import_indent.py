# from AptUrl.Helpers import _
from odoo import _
from odoo import fields, models, api
from datetime import datetime


class Import_Indent(models.Model):
    _name = 'importindent.data'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'customer_name'
    _order = "indent_no desc"

    @api.depends('import_bank_exp_line', 'import_bank_exp_line.expected_total_bank')
    def total_bank(self):
        for rec in self:
            total = 0
            for line in rec.import_bank_exp_line:
                total += line.expected_total_bank
            rec['total_bank_value'] = total

    @api.depends('import_bank_exp_line', 'import_bank_exp_line.actual_bank_exp')
    def actual_total_bank(self):
        for rec in self:
            total = 0
            for line in rec.import_bank_exp_line:
                total += line.actual_bank_exp
            rec['total_bank_actual'] = total

    @api.depends('import_doc_exp_line', 'import_doc_exp_line.expected_total_document')
    def total_doc(self):
        for rec in self:
            total = 0
            for line in rec.import_doc_exp_line:
                total += line.expected_total_document
            rec['total_doc_value'] = total

    @api.depends('import_doc_exp_line', 'import_doc_exp_line.actual_doc_total')
    def actual_total_doc(self):
        for rec in self:
            total = 0
            for line in rec.import_doc_exp_line:
                total += line.actual_doc_total
            rec['total_doc_actual'] = total

    @api.depends('transportation_line', 'transportation_line.expected_total_transportation')
    def total_transportation(self):
        for rec in self:
            total = 0
            for line in rec.transportation_line:
                total += line.expected_total_transportation
            rec['total_transportation_value'] = total

    @api.depends('transportation_line', 'transportation_line.actual_trans_total')
    def actual_total_transportation(self):
        for rec in self:
            total = 0
            for line in rec.transportation_line:
                total += line.actual_trans_total
            rec['total_transportation_actual'] = total

    @api.depends('cnf_line', 'cnf_line.expected_total_cnf')
    def total_cnf(self):
        for rec in self:
            total = 0
            for line in rec.cnf_line:
                total += line.expected_total_cnf
            rec['total_cnf_value'] = total

    @api.depends('cnf_line', 'cnf_line.actual_cnf_total')
    def actual_total_cnf(self):
        for rec in self:
            total = 0
            for line in rec.cnf_line:
                total += line.actual_cnf_total
            rec['total_cnf_actual'] = total

    @api.depends('forwarder_line', 'forwarder_line.expected_total_forwarder')
    def total_forwarder(self):
        for rec in self:
            total = 0
            for line in rec.forwarder_line:
                total += line.expected_total_forwarder
            rec['total_forwarder_value'] = total

    @api.depends('forwarder_line', 'forwarder_line.actual_forwarder_total')
    def actual_total_forwarder(self):
        for rec in self:
            total = 0
            for line in rec.forwarder_line:
                total += line.actual_forwarder_total
            rec['total_forwarder_actual'] = total

    @api.depends('courier_line', 'courier_line.expected_total_courier')
    def total_courier(self):
        for rec in self:
            total = 0
            for line in rec.courier_line:
                total += line.expected_total_courier
            rec['total_courier_value'] = total

    @api.depends('courier_line', 'courier_line.actual_courier_total')
    def actual_total_courier(self):
        for rec in self:
            total = 0
            for line in rec.courier_line:
                total += line.actual_courier_total
            rec['total_courier_actual'] = total

    @api.depends('insurance_line', 'insurance_line.expected_total_insurance')
    def total_insurance(self):
        for rec in self:
            total = 0
            for line in rec.insurance_line:
                total += line.expected_total_insurance
            rec['total_insurance_value'] = total

    @api.depends('insurance_line', 'insurance_line.actual_insurance_total')
    def actual_total_insurance(self):
        for rec in self:
            total = 0
            for line in rec.insurance_line:
                total += line.actual_insurance_total
            rec['total_insurance_actual'] = total

    ########################## Here calculate Final value############################

    @api.depends('total_bank_value', 'total_bank_actual')
    def final_expense_count(self):
        for rec in self:
            rec.final_bank_exp = rec.total_bank_value - rec.total_bank_actual

    @api.depends('total_doc_value', 'total_doc_actual')
    def final_doc_count(self):
        for rec in self:
            rec.final_doc = rec.total_doc_value - rec.total_doc_actual

    @api.depends('total_transportation_value', 'total_transportation_actual')
    def final_transportation_count(self):
        for rec in self:
            rec.final_transportation = rec.total_transportation_value - rec.total_transportation_actual

    @api.depends('total_cnf_value', 'total_cnf_actual')
    def final_cnf_count(self):
        for rec in self:
            rec.final_cnf = rec.total_cnf_value - rec.total_cnf_actual

    @api.depends('total_forwarder_value', 'total_forwarder_actual')
    def final_forwarder_count(self):
        for rec in self:
            rec.final_forwarder = rec.total_forwarder_value - rec.total_forwarder_actual

    @api.depends('total_courier_value', 'total_courier_actual')
    def final_courier_count(self):
        for rec in self:
            rec.final_courier = rec.total_courier_value - rec.total_courier_actual

    @api.depends('total_insurance_value', 'total_insurance_actual')
    def final_insurance_count(self):
        for rec in self:
            rec.final_insurance = rec.total_insurance_value - rec.total_insurance_actual

    ################ Import Indent Field For Form###########################

    customer_name = fields.Many2one('res.partner', string="Customer Name", required=True, track_visibility="always")
    indent_by = fields.Many2one('res.users', string="Indent By", )
    po_no = fields.Integer(string="P.O no", required=True, )
    pi_no = fields.Integer(string="P.I no", required=True, )
    total_invoice_value = fields.Integer(string="Total Invoice Value", required=True, )
    ship_terms = fields.Selection(string="Shipping Terms", selection=[('fob', 'FOB'), ('cnf', 'CNF'), ],
                                  required=True, track_visibility="always")
    ship_by = fields.Selection(string="Shipping By", selection=[('air', 'AIR'), ('sea', 'SEA'), ], required=True,
                               track_visibility="always")
    indent_no = fields.Char(string='Indent No', required=True, copy=False, readonly=True, index=True,
                            default=lambda self: _('New'))
    indent_date = fields.Datetime(string="Indent Date", default=datetime.today(), readonly="True")

    ################ Import Indent Field For Form END ###########################

    ################# Here is One to many Line Code for Form's below page ###############

    import_bank_exp_line = fields.One2many(comodel_name="bank.expense", inverse_name="bank_expense_line",
                                           string="Import Bank Expense", track_visibility="always")
    import_doc_exp_line = fields.One2many(comodel_name="importdocument.expense", inverse_name="doc_expense_line",
                                          string="Import Doc Expense")
    transportation_line = fields.One2many(comodel_name="transportation.cost", inverse_name="transportation_cost_line",
                                          string="Transportation cost Line")
    cnf_line = fields.One2many(comodel_name="cnf.cost", inverse_name="cnf_cost_line",
                               string="Cnf cost Line")
    forwarder_line = fields.One2many(comodel_name="forwarder.cost", inverse_name="forwarder_cost_line",
                                     string="Forwarder cost Line")
    courier_line = fields.One2many(comodel_name="courier.cost", inverse_name="courier_cost_line",
                                   string="Courier cost Line")
    insurance_line = fields.One2many(comodel_name="insurance.cost", inverse_name="insurance_cost_line",
                                     string="Insurance cost Line")
    #################### End One2Many Line  ###################

    ########################Calculation Expected total indent value######################

    total_doc_value = fields.Float(string="Indent Total", compute='total_doc', store=True)
    total_bank_value = fields.Float(string=" Indent Total", compute='total_bank', store=True)
    total_transportation_value = fields.Float(string=" Indent Total", compute='total_transportation', store=True)
    total_cnf_value = fields.Float(string="Indent Total", compute='total_cnf', store=True)
    total_forwarder_value = fields.Float(string="Indent Total", compute='total_forwarder', store=True)
    total_courier_value = fields.Float(string="Indent Total", compute='total_courier', store=True)
    total_insurance_value = fields.Float(string="Indent Total", compute='total_insurance', store=True)
    ########################Calculation Expected total indent value END ######################

    ########################Calculation Actual total Cost indent value######################
    total_bank_actual = fields.Float(string=" Actual Total", compute='actual_total_bank', store=True)
    total_doc_actual = fields.Float(string="Actual Total", compute='actual_total_doc', store=True)
    total_transportation_actual = fields.Float(string=" Actual Total", compute='actual_total_transportation',
                                               store=True)
    total_cnf_actual = fields.Float(string="Actual Total", compute='actual_total_cnf', store=True)
    total_forwarder_actual = fields.Float(string="Actual Total", compute='actual_total_forwarder', store=True)
    total_courier_actual = fields.Float(string=" ActualTotal", compute='actual_total_courier', store=True)
    total_insurance_actual = fields.Float(string="Actual Total", compute='actual_total_insurance', store=True)

    ###################For final Cost calculation#####################

    final_bank_exp = fields.Float(string="Final Amount", compute='final_expense_count', store=True)
    final_doc = fields.Float(string="Final Amount", compute='final_doc_count', store=True)
    final_transportation = fields.Float(string=" Final Amount", compute='final_transportation_count',
                                        store=True)
    final_cnf = fields.Float(string="Final Amount", compute='final_cnf_count', store=True)
    final_forwarder = fields.Float(string="Final Amount", compute='final_forwarder_count', store=True)
    final_courier = fields.Float(string="Final Amount", compute='final_courier_count', store=True)
    final_insurance = fields.Float(string="Final Amount", compute='final_insurance_count', store=True)

    ################### END final Cost calculation#####################

    ############## Serial Number generate code function#################
    @api.model
    def create(self, vals):
        if vals.get('indent_no', _('New')) == _('New'):
            vals['indent_no'] = self.env['ir.sequence'].next_by_code('import.indent.seq') or _('New')
        result = super(Import_Indent, self).create(vals)
        return result


############## END Serial Number generate code function#################


class Bank_expense(models.Model):
    _name = 'bank.expense'
    _description = "Bank Expenses Line"

    # bank_expense = fields.Selection(string="", selection=[('conveyance', 'Conveyance'), ('entertainment',
    # 'Entertainment'), ('print', 'Print'), ('bank_commission', 'Bank commission'), ('swift_charge', 'Swift charge'),
    # ('vat_on_swift_charge', 'Vat On Swift Charge'), ('vat_mergin', 'Vat On Mergin'), ('lc_appli_charge',
    # 'L/C Application form Charge'), ('lcaf_charge', 'LCAF form Charge'), ('amendment_charge', 'Amendment Charge'),
    # ('swift_amendment_charge', 'Swift on Amendment Charge'), ('shipping_gurantee_charge', 'Shipping Gurantee
    # Charge'), ('vat_ship_gurantee', 'VAT on shipping gurantee'), ('stamp', 'Stamp')], required=True,
    # track_visibility="always")
    bank_expense = fields.Many2one(comodel_name="dynamic.field", string="Bank Expense", required=True, )
    bank = fields.Float(related='bank_expense.conf_bank', string="Bank", required=False, track_visibility="always")
    cash = fields.Float(related='bank_expense.conf_cash', string="Cash", required=False, track_visibility="always")
    bank_remarks = fields.Text(string="Remarks")
    actual_bank = fields.Float(string="Actual Bank")
    actual_cash = fields.Float(string="Actual Cash")
    actual_bank_exp = fields.Float(string="Actual Total", compute='count_bank_actual_total', store=True)
    expected_total_bank = fields.Float(string="Expected Total", compute='count_bank_expected_total', store=True)
    bank_expense_line = fields.Many2one('importindent.data', string="Bank Expense Line Id", track_visibility="always")

    @api.depends('bank', 'cash')
    def count_bank_expected_total(self):
        for total in self:
            total.expected_total_bank = total.bank + total.cash

    @api.depends('actual_bank', 'actual_cash')
    def count_bank_actual_total(self):
        for total in self:
            total.actual_bank_exp = total.actual_bank + total.actual_cash


class Import_document_expense(models.Model):
    _name = 'importdocument.expense'
    _description = "Import Document expense Line"

    # import_doc_exp = fields.Selection(string="Import document Expense",
    #                                   selection=[('awb_charge', 'AWB Charge'), ('misc', 'Misc Incorrect Document'), (
    #                                       'misc_bag_wallet', 'Misc Bag or wallet receive with import materials'),
    #                                              ('misc_awb_copy', 'Misc Problem in AWB copy'),
    #                                              ('misc_warehouse_security', 'Misc Import Warehouse security'),
    #                                              ('print', 'Print Or Photocopy')], required=True, )
    import_doc_exp = fields.Many2one(comodel_name="dynamic.importdocuments", string="Import document Expense",
                                     required=True, )
    doc_bank = fields.Float(related='import_doc_exp.conf_doc_bank', string="Bank", required=False, )
    doc_cash = fields.Float(related='import_doc_exp.conf_doc_cash', string="Cash", required=False, )
    actual_doc_bank = fields.Float(string="Actual Bank")
    actual_doc_cash = fields.Float(string="Actual Cash")
    doc_remarks = fields.Text(string="Remarks")
    actual_doc_total = fields.Float(string="Actual Total", compute='count_doc_actual_total', store=True)
    expected_total_document = fields.Float(string="Expected Total", compute='count_doc_expected_total', store=True)
    doc_expense_line = fields.Many2one('importindent.data', string="Doc Expense Line Id")

    @api.depends('doc_bank', 'doc_cash')
    def count_doc_expected_total(self):
        for total in self:
            total.expected_total_document = total.doc_bank + total.doc_cash

    @api.depends('actual_doc_bank', 'actual_doc_cash')
    def count_doc_actual_total(self):
        for total in self:
            total.actual_doc_total = total.actual_doc_bank + total.actual_doc_cash


class Transportation_cost(models.Model):
    _name = 'transportation.cost'
    _description = "Transportation Cost Line"

    # transportation_cost = fields.Selection(string="Transportation Cost",
    #                                        selection=[('carriage_inwards', 'Carriage Inwards'),
    #                                                   ('driver_boksis', 'Driver Boksis'), ], required=True, )
    transportation_cost = fields.Many2one(comodel_name="dynamic.importtransportation", string="Transportation Cost",
                                          required=True, )
    transport_bank = fields.Float(related='transportation_cost.conf_transport_bank', string="Bank")
    transport_cash = fields.Float(related='transportation_cost.conf_transport_cash', string="Cash")

    actual_trans_bank = fields.Float(string="Actual Bank")
    actual_trans_cash = fields.Float(string="Actual Cash")
    transportation_remarks = fields.Text(string="Remarks")
    expected_total_transportation = fields.Float(string="Expected Total", compute='count_transpo_expected_total',
                                                 store=True)
    actual_trans_total = fields.Float(string="Actual Total", compute='count_trans_actual_total', store=True)
    transportation_cost_line = fields.Many2one('importindent.data', string="transportation Line Id")

    @api.depends('transport_bank', 'transport_cash')
    def count_transpo_expected_total(self):
        for total in self:
            total.expected_total_transportation = total.transport_bank + total.transport_cash

    @api.depends('actual_trans_bank', 'actual_trans_cash')
    def count_trans_actual_total(self):
        for total in self:
            total.actual_trans_total = total.actual_trans_bank + total.actual_trans_cash


class Cnf_cost(models.Model):
    _name = 'cnf.cost'
    _description = "C & F cost line"

    # cnf_cost = fields.Selection(string="C & f Cost", selection=[('cf_bill', 'C & f Bill')], required=True, )
    cnf_cost = fields.Many2one(comodel_name="dynamic.importcnf", string="C & f Cost", required=True, )
    cnf_bank = fields.Float(related='cnf_cost.conf_cnf_bank', string="Bank")
    cnf_cash = fields.Float(related='cnf_cost.conf_cnf_cash', string="Cash")

    actual_cnf_bank = fields.Float(string="Actual Bank")
    actual_cnf_cash = fields.Float(string="Actual Cash")
    cnf_remarks = fields.Text(string="Remarks")
    actual_cnf_total = fields.Float(string="Actual Total", compute='count_cnf_actual_total', store=True)
    expected_total_cnf = fields.Float(string="Expected Total", compute='count_transpo_expected_total', store=True)
    cnf_cost_line = fields.Many2one('importindent.data', string="cnf Line Id")

    @api.depends('cnf_bank', 'cnf_cash')
    def count_transpo_expected_total(self):
        for total in self:
            total.expected_total_cnf = total.cnf_bank + total.cnf_cash

    @api.depends('actual_cnf_bank', 'actual_cnf_cash')
    def count_cnf_actual_total(self):
        for total in self:
            total.actual_cnf_total = total.actual_cnf_bank + total.actual_cnf_cash


class Forwarder_cost(models.Model):
    _name = 'forwarder.cost'
    _description = "Forwarder cost line"

    # forwarder_cost = fields.Selection(string="Forwarder Cost", selection=[('forwarder_bill', 'Forwarder Bill')],
    #                                   required=True, )
    forwarder_cost = fields.Many2one(comodel_name="dynamic.importforwarder", string="Forwarder Cost", required=True, )
    forwarder_bank = fields.Float(related='forwarder_cost.conf_forwarder_bank', string="Bank")
    forwarder_cash = fields.Float(related='forwarder_cost.conf_forwarder_cash', string="Cash")
    actual_forwarder_bank = fields.Float(string="Actual Bank")
    actual_forwarder_cash = fields.Float(string="Actual Cash")
    forwarder_remarks = fields.Text(string="Remarks")
    actual_forwarder_total = fields.Float(string="Actual Total", compute='count_forwarder_actual_total', store=True)
    expected_total_forwarder = fields.Float(string="Expected Total", compute='count_forwarder_expected_total',
                                            store=True)
    forwarder_cost_line = fields.Many2one('importindent.data', string="Forwarder Line Id")

    @api.depends('forwarder_bank', 'forwarder_cash')
    def count_forwarder_expected_total(self):
        for total in self:
            total.expected_total_forwarder = total.forwarder_bank + total.forwarder_cash

    @api.depends('actual_forwarder_bank', 'actual_forwarder_cash')
    def count_forwarder_actual_total(self):
        for total in self:
            total.actual_forwarder_total = total.actual_forwarder_bank + total.actual_forwarder_cash


class Courier_charge(models.Model):
    _name = 'courier.cost'
    _description = "Courier Charge line"

    # courier_charge = fields.Selection(string="Courier Charge", selection=[('courier_bill', 'Courier Bill')],
    #                                   required=True, )
    courier_charge = fields.Many2one(comodel_name="dynamic.importcourier", string="Courier Charge", required=True, )
    courier_bank = fields.Float(related='courier_charge.conf_courier_bank', string="Bank")
    courier_cash = fields.Float(related='courier_charge.conf_courier_cash', string="Cash")

    actual_courier_bank = fields.Float(string="Actual Bank")
    actual_courier_cash = fields.Float(string="Actual Cash")
    courier_remarks = fields.Text(string="Remarks")
    actual_courier_total = fields.Float(string="Actual Total", compute='count_courier_actual_total', store=True)
    expected_total_courier = fields.Float(string="Expected Total", compute='count_courier_expected_total', store=True)
    courier_cost_line = fields.Many2one('importindent.data', string="Courier Line Id")

    @api.depends('courier_bank', 'courier_cash')
    def count_courier_expected_total(self):
        for total in self:
            total.expected_total_courier = total.courier_bank + total.courier_cash

    @api.depends('actual_courier_bank', 'actual_courier_cash')
    def count_courier_actual_total(self):
        for total in self:
            total.actual_courier_total = total.actual_courier_bank + total.actual_courier_cash


class Insurance_expense(models.Model):
    _name = 'insurance.cost'
    _description = "Insurance Expense line"

    # insurance_exp = fields.Selection(string="Insurance Expense ", selection=[('insurance-amount', 'Insurance Amount'), ('pay_order_charge', 'Pay Order Charge')], required=True, )

    insurance_exp = fields.Many2one(comodel_name="dynamic.importinsurance", string="Insurance Expense",
                                    required=True, )
    insurance_bank = fields.Float(related='insurance_exp.conf_insurance_bank', string="Bank")
    insurance_cash = fields.Float(related='insurance_exp.conf_insurance_cash', string="Cash")

    actual_insurance_bank = fields.Float(string="Actual Bank")
    actual_insurance_cash = fields.Float(string="Actual Cash")
    insurance_remarks = fields.Text(string="Remarks")
    actual_insurance_total = fields.Float(string="Actual Total", compute='count_insurance_actual_total', store=True)
    expected_total_insurance = fields.Float(string="Expected Total", compute='count_insurance_expected_total',
                                            store=True)
    insurance_cost_line = fields.Many2one('importindent.data', string="insurance Line Id")

    @api.depends('insurance_bank', 'insurance_cash')
    def count_insurance_expected_total(self):
        for total in self:
            total.expected_total_insurance = total.insurance_bank + total.insurance_cash

    @api.depends('actual_insurance_bank', 'actual_insurance_cash')
    def count_insurance_actual_total(self):
        for total in self:
            total.actual_insurance_total = total.actual_insurance_bank + total.actual_insurance_cash
