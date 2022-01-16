from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


class EemBilling(models.Model):
    _name = "eem.billing"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "EEM Management"
    _rec_name = "eem_bill_sequence"

    ################## Compute function for Billing ###################
    @api.depends('entertainment_expense_line_ids', 'entertainment_expense_line_ids.entertainment_bill_amount')
    def compute_entertainment_total(self):
        for rec in self:
            total = 0
            for line in rec.entertainment_expense_line_ids:
                total += line.entertainment_bill_amount
            rec['entertainment_total'] = total

    @api.depends('conveyance_expense_line_ids', 'conveyance_expense_line_ids.conveyance_bill_amount')
    def compute_conveyance_total(self):
        for rec in self:
            total = 0
            for line in rec.conveyance_expense_line_ids:
                total += line.conveyance_bill_amount
            rec['conveyance_total'] = total

    @api.depends('miscellaneous_expense_line_ids', 'miscellaneous_expense_line_ids.miscellaneous_bill_amount')
    def compute_miscellaneous_total(self):
        for rec in self:
            total = 0
            for line in rec.miscellaneous_expense_line_ids:
                total += line.miscellaneous_bill_amount
            rec['miscellaneous_total'] = total

    @api.depends('purchase_expense_line_ids', 'purchase_expense_line_ids.amount')
    def compute_purchase_total(self):
        for rec in self:
            total = 0
            for line in rec.purchase_expense_line_ids:
                total += line.amount
            rec['purchase_total'] = total

    @api.depends('gift_donation_expense_line_ids', 'gift_donation_expense_line_ids.amount')
    def compute_gift_donation_exp_total(self):
        for rec in self:
            total = 0
            for line in rec.gift_donation_expense_line_ids:
                total += line.amount
            rec['gift_donation_exp_total'] = total

    @api.depends('printing_stationery_expense_line_ids', 'printing_stationery_expense_line_ids.amount')
    def compute_printing_stationery_exp_total(self):
        for rec in self:
            total = 0
            for line in rec.printing_stationery_expense_line_ids:
                total += line.amount
            rec['printing_stationery_exp_total'] = total

    @api.depends('entertainment_total', 'conveyance_total', 'miscellaneous_total', 'purchase_total',
                 'gift_donation_exp_total',
                 'printing_stationery_exp_total')
    def compute_total_bill_amount(self):
        for rec in self:
            rec.total_billing_amount = rec.entertainment_total + rec.conveyance_total + rec.miscellaneous_total + \
                                       rec.purchase_total + rec.gift_donation_exp_total + rec.printing_stationery_exp_total

    ################### Compute Function for  Due and Excess Amount ##############
    @api.depends('requested_amount', 'total_billing_amount')
    def compute_due_amount(self):
        for rec in self:
            rec.due_amount = 0
            if rec.requested_amount > rec.total_billing_amount:
                rec.due_amount = rec.requested_amount - rec.total_billing_amount
            elif rec.requested_amount < rec.total_billing_amount:
                rec.due_amount = 0

    @api.depends('requested_amount', 'total_billing_amount')
    def compute_excess_amount(self):
        for rec in self:
            rec.excess_amount = 0
            if rec.total_billing_amount > rec.requested_amount:
                rec.excess_amount = rec.total_billing_amount - rec.requested_amount
            elif rec.requested_amount > rec.total_billing_amount:
                rec.excess_amount = 0

    eem_bill_sequence = fields.Char(string='EEM No :', required=True, copy=False, readonly=True, default=lambda
        self: _('Draft'))  # sequence_id
    user = fields.Many2one('hr.employee', string='Created By :', default=lambda self: self.env.user.employee_id,
                           readonly=True)
    dept = fields.Many2one('hr.department', string='Department :', default=lambda self: self.env.user.department_id,
                           readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employee :',
                                  tracking=True)
    expense_dept = fields.Char(string='Exp Department :', tracking=True)
    reference_id = fields.Many2one('eem.pre_costing', string='Reference :', domain=[('state', '=', 'confirm')],
                                   required=True, tracking=True)
    eem_date = fields.Datetime(string='Bill Create Date :', default=lambda self: fields.datetime.now(),
                               select=True,
                               readonly=True, tracking=True)
    purpose = fields.Text(string='Purpose :', required=True, tracking=True)
    requested_amount = fields.Float(string="Requested Amount :")
    state = fields.Selection([('draft', 'Draft Pre-Costing'), ('confirm', 'Confirm Pre-Costing'),
                              ('draft bill', 'Draft Bill'), ('confirm bill', 'Confirmed Bill'), ('cancel', 'Canceled')],
                             default='draft',
                             string="Status",
                             tracking=True)
    purchase = fields.Boolean(string='Purchase :', default=False, tracking=True)
    miscellaneous = fields.Boolean(string='Miscellaneous :', default=False, tracking=True)
    gift_donation = fields.Boolean(string='Gift & Donation :', default=False, tracking=True)
    printing_stationery = fields.Boolean(string='Printing&Stationery :', default=False, tracking=True)

    # Approval details
    confirm_bill = fields.Char(readonly=True)
    cancel = fields.Char(readonly=True)

    ############### Notebook Line Added field for Billing #####################
    entertainment_expense_line_ids = fields.One2many('entertainment.expense.line', 'EEL_id',
                                                     string='Entertainment Line')
    conveyance_expense_line_ids = fields.One2many('conveyance.expense.line', 'CEL_id', string='Conveyance Line')
    miscellaneous_expense_line_ids = fields.One2many('miscellaneous.expense.line', 'MEL_id', string='Miscellaneous '
                                                                                                    'Line')
    purchase_expense_line_ids = fields.One2many('purchase.expense.line', 'purchase_expense_id', string='Purchase '
                                                                                                       'Line')
    gift_donation_expense_line_ids = fields.One2many('gift_donation.expense.line', 'gift_donation_exp_id',
                                                     string='Gift & Donation Line')
    printing_stationery_expense_line_ids = fields.One2many('printing_stationery.expense.line',
                                                           'printing_stationery_exp_id')
    #################### Computed Field ##################
    entertainment_total = fields.Float(string='Entertainment Total',
                                       compute='compute_entertainment_total')
    conveyance_total = fields.Float(string='Conveyance Total',
                                    compute='compute_conveyance_total')
    miscellaneous_total = fields.Float(string='Miscellaneous Total',
                                       compute='compute_miscellaneous_total')
    purchase_total = fields.Float(string='Purchase Total',
                                  compute='compute_purchase_total')
    gift_donation_exp_total = fields.Float(string='Gift&Donation Total',
                                           compute='compute_gift_donation_exp_total')
    printing_stationery_exp_total = fields.Float(string='Printing & Stationery Total',
                                                 compute='compute_printing_stationery_exp_total')
    total_billing_amount = fields.Float(string='Total Bill Amount',
                                        compute='compute_total_bill_amount')
    due_amount = fields.Float('Unutilized Amount', compute='compute_due_amount')
    excess_amount = fields.Float('Excess Bill Amount', compute='compute_excess_amount')

    ################ Confirm Button Action #################
    def action_confirm_bill(self):
        user_id = self.env.user
        emp_id = self.env['hr.employee'].search([('name', '=', user_id.name)])
        for rec in self:
            temp = "Bill Confirmed By : " + user_id.name + "; " + "Department : " + \
                   emp_id.department_id.name + " at " + str(
                fields.datetime.now())
            rec.confirm_bill = temp
            rec.state = 'confirm bill'
            return fields.Date.context_today(self)

    def action_bill_cancel(self):
        user_id = self.env.user
        emp_id = self.env['hr.employee'].search([('name', '=', user_id.name)])
        for rec in self:
            temp = "Canceled By : " + user_id.name + "; " + "Department : " + str(emp_id.department_id.name) + " at " \
                   + str(
                fields.datetime.now())
            rec.cancel = temp
            rec.state = 'cancel'
            return

    # sequence value
    @api.model
    def create(self, vals):
        if vals.get('eem_bill_sequence', _('Draft')) == _('Draft'):
            vals['eem_bill_sequence'] = self.env['ir.sequence'].next_by_code('eem.billing') or _(
                'Draft')  # sequence value
        res = super(EemBilling, self).create(vals)
        return res

    # Get automatic department after selecting employee
    @api.onchange('employee_id')
    def onchange_employee_id(self):
        if self.employee_id:
            if self.employee_id.department_id.name:
                self.expense_dept = self.employee_id.department_id.name
        else:
            self.expense_dept = ''

    @api.onchange('reference_id')
    def onchange_reference_id(self):
        if self.reference_id:
            if self.reference_id.employee_id:
                self.employee_id = self.reference_id.employee_id
            if self.reference_id.expense_dept:
                self.expense_dept = self.reference_id.expense_dept
            if self.reference_id.purpose:
                self.purpose = self.reference_id.purpose
            if self.reference_id.total_pre_costing_amount:
                self.requested_amount = self.reference_id.total_pre_costing_amount
            if self.reference_id.purchase:
                self.purchase = self.reference_id.purchase
            if self.reference_id.miscellaneous:
                self.miscellaneous = self.reference_id.miscellaneous
            if self.reference_id.gift_donation:
                self.gift_donation = self.reference_id.gift_donation
            if self.reference_id.printing_stationery:
                self.printing_stationery = self.reference_id.printing_stationery

        else:
            self.employee_id = ''
            self.expense_dept = ''
            self.purpose = ''
            self.purchase = ''
            self.miscellaneous = ''
            self.gift_donation = ''
            self.printing_stationery = ''

    @api.onchange('reference_id')
    def onchange_entertainment_reference_id(self):
        for rec in self:
            lines = [(5, 0, 0)]
            for line in self.reference_id.entertainment_pre_costing_line_ids:
                val = {
                    'product_id': line.product_id,
                    'remark': line.remark
                }
                lines.append((0, 0, val))
            rec.entertainment_expense_line_ids = lines

    @api.onchange('reference_id')
    def onchange_conv_reference_id(self):
        for rec in self:
            lines = [(5, 0, 0)]
            for line in self.reference_id.conveyance_pre_costing_line_ids:
                val = {
                    'product_id': line.product_id,
                    'remark': line.remark
                }
                lines.append((0, 0, val))
            rec.conveyance_expense_line_ids = lines

    @api.onchange('reference_id')
    def onchange_mis_reference_id(self):
        for rec in self:
            lines = [(5, 0, 0)]
            for line in self.reference_id.miscellaneous_pre_costing_line_ids:
                val = {
                    'product_id': line.product_id,
                    'designation': line.designation,
                    'miscellaneous_bill_amount': line.amount,
                    'remark': line.remark
                }
                lines.append((0, 0, val))
            rec.miscellaneous_expense_line_ids = lines

    @api.onchange('reference_id')
    def onchange_purchase_reference_id(self):
        for rec in self:
            lines = [(5, 0, 0)]
            for line in self.reference_id.purchase_pre_costing_line_ids:
                val = {
                    'purchase_ref_no': line.purchase_ref_no,
                    'amount': line.amount,
                    'remark': line.remark
                }
                lines.append((0, 0, val))
            rec.purchase_expense_line_ids = lines

    @api.onchange('reference_id')
    def onchange_gift_donation_reference_id(self):
        for rec in self:
            lines = [(5, 0, 0)]
            for line in self.reference_id.gift_donation_pre_costing_line_ids:
                val = {
                    'product_id': line.product_id,
                    'description': line.description,
                    'amount': line.amount,
                    'remark': line.remark
                }
                lines.append((0, 0, val))
            rec.gift_donation_expense_line_ids = lines

    @api.onchange('reference_id')
    def onchange_printing_stationery_reference_id(self):
        for rec in self:
            lines = [(5, 0, 0)]
            for line in self.reference_id.printing_stationery_pre_costing_line_ids:
                val = {
                    'product_id': line.product_id,
                    'description': line.description,
                    'amount': line.amount,
                    'remark': line.remark
                }
                lines.append((0, 0, val))
            rec.printing_stationery_expense_line_ids = lines


####### Notebook model for Billing #######
class EntertainmentExpenseLine(models.Model):
    _name = "entertainment.expense.line"
    _description = "Entertainment Expense Lines"

    # Computed function
    @api.depends('req_qty', 'unit_cost')
    def _get_entertainment_bill_amount(self):
        for rec in self:
            rec.entertainment_bill_amount = rec.req_qty * rec.unit_cost

    EEL_id = fields.Many2one('eem.billing', string='EEL')
    product_id = fields.Many2one('eem.product', string='Product', domain=[('is_entertainment', '=', True)],
                                 change_default=True, required=True, tracking=True)  # Category based product
    req_qty = fields.Integer(string="Quantity ", required=True, tracking=True)
    unit_cost = fields.Float(string="Unit Price", tracking=True)
    payment_date = fields.Date(string='Payment Date', tracking=True)
    entertainment_bill_amount = fields.Float(string='Bill Amount', compute='_get_entertainment_bill_amount',
                                             store=True, tracking=True)
    remark = fields.Char(string='Remarks')

    # Get unit cost of any product after selecting the product
    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            if self.product_id.unit_cost:
                self.unit_cost = self.product_id.unit_cost
        else:
            self.unit_cost = ''


class ConveyanceExpenseLine(models.Model):
    _name = "conveyance.expense.line"
    _description = "Conveyance Expense Lines"

    CEL_id = fields.Many2one('eem.billing', string='CEL')
    product_id = fields.Many2one('eem.product', string='Product', domain=[('is_conveyance', '=', True)],
                                 change_default=True, required=True, tracking=True)
    con_from = fields.Char(string="From", required=True, tracking=True)
    con_to = fields.Char(string="Destination", required=True, tracking=True)
    payment_date = fields.Date(string='Payment Date', tracking=True)
    conveyance_bill_amount = fields.Float(string='Bill Amount', tracking=True)
    remark = fields.Char(string='Remarks')


class MiscellaneousExpenseLine(models.Model):
    _name = "miscellaneous.expense.line"
    _description = "Miscellaneous Expense Lines"

    MEL_id = fields.Many2one('eem.billing', string='CEL')
    product_id = fields.Many2one('eem.product', string='Product', domain=[('is_miscellaneous', '=',
                                                                           True)],
                                 change_default=True, required=True, tracking=True)
    name = fields.Char(string='Name', tracking=True)
    designation = fields.Char(string='Designation', required=True, tracking=True)
    dept = fields.Char(string='Department', tracking=True)
    dist = fields.Char(string='Home District', tracking=True)
    phone = fields.Char(string='Phone No', tracking=True)
    payment_date = fields.Date(string='Payment Date', required=True, tracking=True)
    work_place = fields.Char(string='Place of Work', tracking=True)
    miscellaneous_bill_amount = fields.Float(string='Bill Amount', tracking=True)
    purpose = fields.Text(string='Purpose', tracking=True)
    remark = fields.Char(string='Remarks')

    # @api.constrains('payment_date')
    # def _check_payment_date(self):
    #     for rec in self:
    #         if rec.payment_date < fields.Date.today():
    #             raise ValidationError("The Payment date cannot be set in the past !!\n --- প্রয়োজনীয় তারিখ অতীতে "
    #                                   "সেট "
    #                                   "করা যাবে না ---|")


class PurchaseExpenseLine(models.Model):
    _name = "purchase.expense.line"
    _description = "Purchase Expense Lines"

    purchase_expense_id = fields.Many2one('eem.billing', string='Purchase Expanse:')
    purchase_ref_no = fields.Char(string='Purchase Ref. No', tracking=True)
    amount = fields.Float(string='Amount', tracking=True)
    remark = fields.Char(string='Remarks')


class GiftDonationExpenseLine(models.Model):
    _name = "gift_donation.expense.line"
    _description = "Gift & Donation Expense Lines"

    gift_donation_exp_id = fields.Many2one('eem.billing', string='Gift & Donation Expense:')
    product_id = fields.Many2one('eem.product', string='Service Name', domain=[('is_gift_donation', '=', True)],
                                 change_default=True, tracking=True)  # Category based product
    description = fields.Text(string='Description')
    amount = fields.Float(string='Amount')
    remark = fields.Char(string='Remarks')


class PrintingStationeryExpenseLine(models.Model):
    _name = "printing_stationery.expense.line"
    _description = "Printing & Stationery Expense Lines"

    printing_stationery_exp_id = fields.Many2one('eem.billing', string='Printing & Stationery Pre-Costing:')
    product_id = fields.Many2one('eem.product', string='Product Name', domain=[('is_printing_stationery', '=', True)],
                                 change_default=True, tracking=True)  # Category based product
    description = fields.Text(string='Description')
    amount = fields.Float(string='Amount')
    remark = fields.Char(string='Remarks')
