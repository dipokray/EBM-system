from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


class EbmManagement(models.Model):
    _name = "ebm.management"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "EBM Management"
    _rec_name = "ebm_sequence"

    ################ Compute function for pre-costing ##############
    @api.depends('entertainment_pre_costing_line_ids', 'entertainment_pre_costing_line_ids.amount')
    def compute_entertainment_pre_costing_total(self):
        for rec in self:
            total = 0
            for line in rec.entertainment_pre_costing_line_ids:
                total += line.amount
            rec['entertainment_pre_costing_total'] = total

    @api.depends('conveyance_pre_costing_line_ids', 'conveyance_pre_costing_line_ids.amount')
    def compute_conveyance_pre_costing_total(self):
        for rec in self:
            total = 0
            for line in rec.conveyance_pre_costing_line_ids:
                total += line.amount
            rec['conveyance_pre_costing_total'] = total

    @api.depends('miscellaneous_pre_costing_line_ids', 'miscellaneous_pre_costing_line_ids.amount')
    def compute_miscellaneous_pre_costing_total(self):
        for rec in self:
            total = 0
            for line in rec.miscellaneous_pre_costing_line_ids:
                total += line.amount
            rec['miscellaneous_pre_costing_total'] = total

    @api.depends('purchase_pre_costing_line_ids', 'purchase_pre_costing_line_ids.amount')
    def compute_purchase_pre_costing_total(self):
        for rec in self:
            total = 0
            for line in rec.purchase_pre_costing_line_ids:
                total += line.amount
            rec['purchase_pre_costing_total'] = total

    @api.depends('entertainment_pre_costing_total', 'conveyance_pre_costing_total', 'miscellaneous_pre_costing_total',
                 'purchase_pre_costing_total')
    def compute_total_pre_costing_amount(self):
        for rec in self:
            rec.total_pre_costing_amount = rec.entertainment_pre_costing_total + rec.conveyance_pre_costing_total + \
                                           rec.miscellaneous_pre_costing_total + rec.purchase_pre_costing_total

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

    @api.depends('entertainment_total', 'conveyance_total', 'miscellaneous_total', 'purchase_total')
    def compute_total_bill_amount(self):
        for rec in self:
            rec.total_billing_amount = rec.entertainment_total + rec.conveyance_total + rec.miscellaneous_total + rec.purchase_total

    ################### Compute Function for  Due and Excess Amount ##############
    @api.depends('total_pre_costing_amount', 'total_billing_amount')
    def compute_due_amount(self):
        for rec in self:
            rec.due_amount = 0
            if rec.total_pre_costing_amount > rec.total_billing_amount:
                rec.due_amount = rec.total_pre_costing_amount - rec.total_billing_amount
            elif rec.total_pre_costing_amount < rec.total_billing_amount:
                rec.due_amount = 0

    @api.depends('total_pre_costing_amount', 'total_billing_amount')
    def compute_excess_amount(self):
        for rec in self:
            rec.excess_amount = 0
            if rec.total_billing_amount > rec.total_pre_costing_amount:
                rec.excess_amount = rec.total_billing_amount - rec.total_pre_costing_amount
            elif rec.total_pre_costing_amount > rec.total_billing_amount:
                rec.excess_amount = 0

    ########### Pre-costing to bill difference ###########
    @api.depends('entertainment_pre_costing_total', 'entertainment_total')
    def compute_entertainment_difference(self):
        for rec in self:
            rec.entertainment_difference = rec.entertainment_pre_costing_total - rec.entertainment_total

    @api.depends('conveyance_pre_costing_total', 'conveyance_total')
    def compute_conveyance_difference(self):
        for rec in self:
            rec.conveyance_difference = rec.conveyance_pre_costing_total - rec.conveyance_total

    @api.depends('miscellaneous_pre_costing_total', 'miscellaneous_total')
    def compute_miscellaneous_difference(self):
        for rec in self:
            rec.miscellaneous_difference = rec.miscellaneous_pre_costing_total - rec.miscellaneous_total

    @api.depends('purchase_pre_costing_total', 'purchase_total')
    def compute_purchase_difference(self):
        for rec in self:
            rec.purchase_difference = rec.purchase_pre_costing_total - rec.purchase_total

    ebm_sequence = fields.Char(string='EBM No :', required=True, copy=False, readonly=True, default=lambda
        self: _('New'))  # sequence_id
    user = fields.Many2one('hr.employee', string='Created By :', default=lambda self: self.env.user.employee_id,
                           readonly=True)
    dept = fields.Many2one('hr.department', string='Department :', default=lambda self: self.env.user.department_id,
                           readonly=True)
    # expense_dept_for = fields.Selection([
    #     ('own', 'Own'),
    #     ('other', 'Other'),
    # ], string='Expense For :', required=True, default='own', tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Employee :', default=lambda self: self.env.user.employee_id,
                                  tracking=True)
    expense_dept = fields.Char(string='Exp Department :', tracking=True)
    ebm_date = fields.Datetime(string='EBM Create Date :', default=datetime.today(), readonly=True, tracking=True)
    required_date = fields.Date(string='Required Date :', required=True, tracking=True)
    purpose = fields.Text(string='Purpose :', required=True, tracking=True)
    state = fields.Selection([('draft', 'Draft Pre-Costing'), ('confirm', 'Confirm Pre-Costing'), ('department '
                                                                                                   'manager',
                                                                                                   'Department Manager'),
                              ('audit',
                               'Audit'),
                              ('account', 'Account'), ('management', 'Management Approved'),
                              ('draft bill', 'Draft Bill'), ('confirm bill', 'Confirm Bill'),
                              ('department manager bill', 'Department '
                                                          'Manager '),
                              ('audit bill',
                               'Audit'),
                              ('account bill', 'Account'), ('management bill', 'Management')],
                             default='draft',
                             string="Status",
                             tracking=True)
    purchase = fields.Boolean(string='Purchase :', default=False, tracking=True)
    miscellaneous = fields.Boolean(string='Miscellaneous :', default=False, tracking=True)

    # Approval details
    confirm_pre_costing = fields.Char(readonly=True)
    confirm_bill = fields.Char(readonly=True)
    department_approve = fields.Char(readonly=True)
    audit_approve = fields.Char(readonly=True)
    account_approve = fields.Char(readonly=True)
    management_approve = fields.Char(readonly=True)

    ############# Notebook Line Added field for pre-costing ##################
    entertainment_pre_costing_line_ids = fields.One2many(
        'entertainment.pre_costing.lines', 'entertainment_pre_costing_id', string='Entertainment Pre-Costing Line')
    conveyance_pre_costing_line_ids = fields.One2many(
        'conveyance.pre_costing.lines', 'conveyance_pre_costing_id', string='Conveyance Pre-Costing Line')
    miscellaneous_pre_costing_line_ids = fields.One2many(
        'miscellaneous.pre_costing.lines', 'miscellaneous_pre_costing_id', string='Miscellaneous Pre-Costing Line')
    purchase_pre_costing_line_ids = fields.One2many('purchase.pre_costing.lines', 'purchase_pre_costing_id'
                                                    )
    ############### Notebook Line Added field for Billing #####################
    entertainment_expense_line_ids = fields.One2many('entertainment.expense.lines', 'EEL_id',
                                                     string='Entertainment Line')
    conveyance_expense_line_ids = fields.One2many('conveyance.expense.lines', 'CEL_id', string='Conveyance Line')
    miscellaneous_expense_line_ids = fields.One2many('miscellaneous.expense.lines', 'MEL_id', string='Miscellaneous '
                                                                                                     'Line')
    purchase_expense_line_ids = fields.One2many('purchase.expense.lines', 'purchase_expense_id', string='Purchase '
                                                                                                        'Line')
    #################### Computed Field ##################
    entertainment_pre_costing_total = fields.Float(string='Entertainment Total',
                                                   compute='compute_entertainment_pre_costing_total')
    conveyance_pre_costing_total = fields.Float(string='Conveyance Total',
                                                compute='compute_conveyance_pre_costing_total')
    miscellaneous_pre_costing_total = fields.Float(string='Miscellaneous Total',
                                                   compute='compute_miscellaneous_pre_costing_total')
    purchase_pre_costing_total = fields.Float(string='Purchase Total',
                                              compute='compute_purchase_pre_costing_total')
    total_pre_costing_amount = fields.Float(string='Total Pre-Costing Amount',
                                            compute='compute_total_pre_costing_amount')
    entertainment_total = fields.Float(string='Entertainment Total',
                                       compute='compute_entertainment_total')
    conveyance_total = fields.Float(string='Conveyance Total',
                                    compute='compute_conveyance_total')
    miscellaneous_total = fields.Float(string='Miscellaneous Total',
                                       compute='compute_miscellaneous_total')
    purchase_total = fields.Float(string='Purchase Total',
                                  compute='compute_purchase_total')
    entertainment_difference = fields.Float(string='Entertainment Difference :',
                                            compute='compute_entertainment_difference')
    conveyance_difference = fields.Float(string='Conveyance Difference :',
                                         compute='compute_conveyance_difference')
    miscellaneous_difference = fields.Float(string='miscellaneous Difference :',
                                            compute='compute_miscellaneous_difference')
    purchase_difference = fields.Float(string='purchase Difference :',
                                       compute='compute_purchase_difference')
    total_billing_amount = fields.Float(string='Total Bill Amount',
                                        compute='compute_total_bill_amount')

    due_amount = fields.Float('Unutilized Amount', compute='compute_due_amount')
    excess_amount = fields.Float('Excess Bill Amount', compute='compute_excess_amount')

    def action_confirm_pre_costing(self):
        user_id = self.env.user
        emp_id = self.env['hr.employee'].search([('name', '=', user_id.name)])
        for rec in self:
            temp = "Confirmed By : " + user_id.name + "; " + "Department : " + emp_id.department_id.name + " at " + str(
                fields.datetime.now())
            rec.confirm_pre_costing = temp
            rec.state = 'confirm'
            return fields.Date.context_today(self)

    def action_department(self):
        user_id = self.env.user
        emp_id = self.env['hr.employee'].search([('name', '=', user_id.name)])
        for rec in self:
            temp = "Approved By : Department Manager :" + " " + user_id.name + "; " + "Department : " + \
                   emp_id.department_id.name + " " + "at" + str(fields.datetime.now())
            rec.department_approve = temp
            rec.state = 'department manager'
            return fields.Date.context_today(self)

    def action_audit(self):
        user_id = self.env.user
        emp_id = self.env['hr.employee'].search([('name', '=', user_id.name)])
        for rec in self:
            temp = "Approved By : Audit manager : " + user_id.name + "; " + "Department : " + emp_id.department_id.name + " at " + str(
                fields.datetime.now())
            rec.audit_approve = temp
            rec.state = 'audit'
            return fields.Date.context_today(self)

    def action_account(self):
        user_id = self.env.user
        emp_id = self.env['hr.employee'].search([('name', '=', user_id.name)])
        for rec in self:
            temp = "Approved By : Account manager : " + user_id.name + "; " + "Department : " + \
                   emp_id.department_id.name + " at " + str(
                fields.datetime.now())
            rec.account_approve = temp
            rec.state = 'account'
            return fields.Date.context_today(self)

    def action_management(self):
        user_id = self.env.user
        emp_id = self.env['hr.employee'].search([('name', '=', user_id.name)])
        for rec in self:
            temp = "Approved By : Management : " + user_id.name + "; " + "Department : " + emp_id.department_id.name + \
                   " at " + str(
                fields.datetime.now())
            rec.management_approve = temp
            rec.state = 'management'
            return fields.Date.context_today(self)

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_draft_bill(self):
        user_id = self.env.user
        emp_id = self.env['hr.employee'].search([('name', '=', user_id.name)])
        for rec in self:
            temp = "Bill Draft By : " + user_id.name + "; " + "Department : " + emp_id.department_id.name + " " + "at " + str(
                fields.datetime.now())
            rec.management_approve = temp
            rec.state = 'draft bill'
            return fields.Date.context_today(self)

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

    def action_department_bill_conf(self):
        user_id = self.env.user
        emp_id = self.env['hr.employee'].search([('name', '=', user_id.name)])
        for rec in self:
            temp = "Approved By : Department manager : " + user_id.name + "; " + "Department : " + \
                   emp_id.department_id.name + \
                   " at " + str(fields.datetime.now())
            rec.management_approve = temp
            rec.state = 'department manager bill'
            return fields.Date.context_today(self)

    def action_audit_bill_conf(self):
        user_id = self.env.user
        emp_id = self.env['hr.employee'].search([('name', '=', user_id.name)])
        for rec in self:
            temp = "Bill Approved By : Audit manager : " + user_id.name + "; " + "Department : " + \
                   emp_id.department_id.name + " at " + str(
                fields.datetime.now())
            rec.management_approve = temp
            rec.state = 'audit bill'
            return fields.Date.context_today(self)

    def action_account_bill_conf(self):
        user_id = self.env.user
        emp_id = self.env['hr.employee'].search([('name', '=', user_id.name)])
        for rec in self:
            temp = "Bill Approved By : Account manager : " + user_id.name + "; " + "Department : " + \
                   emp_id.department_id.name + " at " + str(
                fields.datetime.now())
            rec.account_approve = temp
            rec.state = 'account bill'
            return fields.Date.context_today(self)

    def action_management_bill_conf(self):
        user_id = self.env.user
        emp_id = self.env['hr.employee'].search([('name', '=', user_id.name)])
        for rec in self:
            temp = "Bill Approved By : Management : " + user_id.name + "; " + "Department : " + \
                   emp_id.department_id.name + " at " + str(fields.datetime.now())
            rec.management_approve = temp
            rec.state = 'management bill'
            return fields.Date.context_today(self)

    # sequence value
    @api.model
    def create(self, vals):
        if vals.get('ebm_sequence', _('New')) == _('New'):
            vals['ebm_sequence'] = self.env['ir.sequence'].next_by_code('ebm.management') or _(
                'New')  # sequence value
        res = super(EbmManagement, self).create(vals)
        return res

    # # field validation
    # @api.constrains('requested_amount')
    # def check_requested_amount(self):
    #     for rec in self:
    #         if rec.requested_amount == 0:
    #             raise ValidationError(
    #                 _("Please Enter Correct Amount. Amount can not be Zero !!\n ---- দয়া করে সঠিক পরিমাণ লিখুন "
    #                   "----!"))

    # # Date field validation
    # @api.constrains('required_date')
    # def _check_required_date(self):
    #     for rec in self:
    #         if rec.required_date < fields.Date.today():
    #             raise ValidationError("The Required date cannot be set in the past !!\n --- প্রয়োজনীয় তারিখ অতীতে "
    #                                   "সেট "
    #                                   "করা যাবে না ---|")

    # Get automatic department after selecting employee
    @api.onchange('employee_id')
    def onchange_employee_id(self):
        if self.employee_id:
            if self.employee_id.department_id.name:
                self.expense_dept = self.employee_id.department_id.name
        else:
            self.expense_dept = ''

    ###### Notebook for Pre-costing ######


class EntertainmentPreCostingLines(models.Model):
    _name = "entertainment.pre_costing.lines"
    _description = "Entertainment Pre-Costing Lines"

    entertainment_pre_costing_id = fields.Many2one('ebm.management', string='Entertainment Pre-Costing:')
    product_id = fields.Many2one('ebm.product', string='Product', domain=[('is_entertainment', '=', True)],
                                 tracking=True)  # Category based product
    amount = fields.Float(string='Amount', tracking=True)
    remark = fields.Char(string='Remarks')

    # Get unit cost of any product after selecting the product
    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            if self.product_id.unit_cost:
                self.amount = self.product_id.unit_cost
        else:
            self.amount = ''


class ConveyancePreCostingLines(models.Model):
    _name = "conveyance.pre_costing.lines"
    _description = "Conveyance Pre-Costing Lines"

    conveyance_pre_costing_id = fields.Many2one('ebm.management', string='Conveyance Pre-Costing:')
    product_id = fields.Many2one('ebm.product', string='Product', domain=[('is_conveyance', '=', True)],
                                 change_default=True, tracking=True)  # Category based product
    amount = fields.Float(string='Amount', tracking=True)
    remark = fields.Char(string='Remarks')


class MiscellaneousPreCostingLines(models.Model):
    _name = "miscellaneous.pre_costing.lines"
    _description = "Miscellaneous Pre-Costing Lines"

    miscellaneous_pre_costing_id = fields.Many2one('ebm.management', string='Miscellaneous Pre-Costing:')
    product_id = fields.Many2one('ebm.product', string='Product', domain=[('is_miscellaneous', '=', True)],
                                 change_default=True, tracking=True)  # Category based product
    amount = fields.Float(string='Amount', tracking=True)
    remark = fields.Char(string='Remarks')


class PurchasePreCostingLines(models.Model):
    _name = "purchase.pre_costing.lines"
    _description = "Purchase Pre-Costing Lines"

    purchase_pre_costing_id = fields.Many2one('ebm.management', string='Purchase Pre-Costing:')
    purchase_ref_no = fields.Char(string='Purchase Ref. No', tracking=True)
    amount = fields.Float(string='Amount', tracking=True)
    remark = fields.Char(string='Remarks')


######## Notebook model for Entertainment ##########
class EntertainmentExpenseLines(models.Model):
    _name = "entertainment.expense.lines"
    _description = "Entertainment Expense Lines"

    # Computed function
    @api.depends('req_qty', 'unit_cost')
    def _get_entertainment_bill_amount(self):
        for rec in self:
            rec.entertainment_bill_amount = rec.req_qty * rec.unit_cost

    EEL_id = fields.Many2one('ebm.management', string='EEL')
    product_id = fields.Many2one('ebm.product', string='Product', domain=[('is_entertainment', '=', True)],
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


####### Notebook model for Conveyance #######
class ConveyanceExpenseLines(models.Model):
    _name = "conveyance.expense.lines"
    _description = "Conveyance Expense Lines"

    CEL_id = fields.Many2one('ebm.management', string='CEL')
    product_id = fields.Many2one('ebm.product', string='Product', domain=[('is_conveyance', '=', True)],
                                 change_default=True, required=True, tracking=True)
    con_from = fields.Char(string="From", required=True, tracking=True)
    con_to = fields.Char(string="Destination", required=True, tracking=True)
    payment_date = fields.Date(string='Payment Date', tracking=True)
    conveyance_bill_amount = fields.Float(string='Bill Amount', tracking=True)
    remark = fields.Char(string='Remarks')


######## Notebook model for Miscellaneous ########
class MiscellaneousExpenseLines(models.Model):
    _name = "miscellaneous.expense.lines"
    _description = "Miscellaneous Expense Lines"

    MEL_id = fields.Many2one('ebm.management', string='CEL')
    product_id = fields.Many2one('ebm.product', string='Product', domain=[('is_miscellaneous', '=',
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

    @api.constrains('payment_date')
    def _check_payment_date(self):
        for rec in self:
            if rec.payment_date < fields.Date.today():
                raise ValidationError("The Payment date cannot be set in the past !!\n --- প্রয়োজনীয় তারিখ অতীতে "
                                      "সেট "
                                      "করা যাবে না ---|")


class PurchaseExpenseLines(models.Model):
    _name = "purchase.expense.lines"
    _description = "Purchase Expense Lines"

    purchase_expense_id = fields.Many2one('ebm.management', string='Purchase Expanse:')
    purchase_ref_no = fields.Char(string='Purchase Ref. No', tracking=True)
    amount = fields.Float(string='Amount', tracking=True)
    remark = fields.Char(string='Remarks')
