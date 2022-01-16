from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


class EemPrecosting(models.Model):
    _name = "eem.pre_costing"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "EEM Management"
    _rec_name = "eem_sequence"

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

    @api.depends('gift_donation_pre_costing_line_ids', 'gift_donation_pre_costing_line_ids.amount')
    def compute_gift_donation_pre_costing_total(self):
        for rec in self:
            total = 0
            for line in rec.gift_donation_pre_costing_line_ids:
                total += line.amount
            rec['gift_donation_pre_costing_total'] = total

    @api.depends('printing_stationery_pre_costing_line_ids', 'printing_stationery_pre_costing_line_ids.amount')
    def compute_printing_stationery_pre_costing_total(self):
        for rec in self:
            total = 0
            for line in rec.printing_stationery_pre_costing_line_ids:
                total += line.amount
            rec['printing_stationery_pre_costing_total'] = total

    @api.depends('entertainment_pre_costing_total', 'conveyance_pre_costing_total', 'miscellaneous_pre_costing_total',
                 'purchase_pre_costing_total', 'gift_donation_pre_costing_total',
                 'printing_stationery_pre_costing_total')
    def compute_total_pre_costing_amount(self):
        for rec in self:
            rec.total_pre_costing_amount = rec.entertainment_pre_costing_total + rec.conveyance_pre_costing_total + \
                                           rec.miscellaneous_pre_costing_total + rec.purchase_pre_costing_total + \
                                           rec.gift_donation_pre_costing_total + rec.printing_stationery_pre_costing_total

    eem_sequence = fields.Char(string='EEM No :', required=True, copy=False, readonly=True, default=lambda
        self: _('Draft'))  # sequence_id
    user = fields.Many2one('hr.employee', string='Created By :', default=lambda self: self.env.user.employee_id,
                           readonly=True)
    dept = fields.Many2one('hr.department', string='Department :', default=lambda self: self.env.user.department_id,
                           readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employee :', default=lambda self: self.env.user.employee_id,
                                  tracking=True)
    expense_dept = fields.Char(string='Exp Department :', tracking=True)
    eem_date = fields.Datetime(string='EBE Create Date :', default=lambda self: fields.datetime.now(), select=True,
                               readonly=True, tracking=True)
    required_date = fields.Date(string='Required Date :', required=True, tracking=True)
    purpose = fields.Text(string='Purpose :', required=True, tracking=True)
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
    confirm_pre_costing = fields.Char(readonly=True)
    cancel = fields.Char(readonly=True)

    ############# Notebook Line Added field for pre-costing ##################
    entertainment_pre_costing_line_ids = fields.One2many(
        'entertainment.pre_costing.line', 'entertainment_pre_costing_id', string='Entertainment Pre-Costing Line')
    conveyance_pre_costing_line_ids = fields.One2many(
        'conveyance.pre_costing.line', 'conveyance_pre_costing_id', string='Conveyance Pre-Costing Line')
    miscellaneous_pre_costing_line_ids = fields.One2many(
        'miscellaneous.pre_costing.line', 'miscellaneous_pre_costing_id', string='Miscellaneous Pre-Costing Line')
    purchase_pre_costing_line_ids = fields.One2many('purchase.pre_costing.line', 'purchase_pre_costing_id')
    gift_donation_pre_costing_line_ids = fields.One2many('gift_donation.pre_costing.line',
                                                         'gift_donation_pre_costing_id'
                                                         )
    printing_stationery_pre_costing_line_ids = fields.One2many('printing_stationery.pre_costing.line',
                                                               'printing_stationery_pre_costing_id'
                                                               )
    #################### Computed Field ##################
    entertainment_pre_costing_total = fields.Float(string='Entertainment Total',
                                                   compute='compute_entertainment_pre_costing_total')
    conveyance_pre_costing_total = fields.Float(string='Conveyance Total',
                                                compute='compute_conveyance_pre_costing_total')
    miscellaneous_pre_costing_total = fields.Float(string='Miscellaneous Total',
                                                   compute='compute_miscellaneous_pre_costing_total')
    purchase_pre_costing_total = fields.Float(string='Purchase Total',
                                              compute='compute_purchase_pre_costing_total')
    gift_donation_pre_costing_total = fields.Float(string='Gift&Donation Total',
                                                   compute='compute_gift_donation_pre_costing_total')
    printing_stationery_pre_costing_total = fields.Float(string='Printing & Stationery Total',
                                                         compute='compute_printing_stationery_pre_costing_total')
    total_pre_costing_amount = fields.Float(string='Total Pre-Costing Amount',
                                            compute='compute_total_pre_costing_amount')

    ################ Button Action #################
    def action_confirm_pre_costing(self):
        user_id = self.env.user
        emp_id = self.env['hr.employee'].search([('name', '=', user_id.name)])
        for rec in self:
            temp = "Confirmed By : " + user_id.name + "; " + "Department : " + str(
                emp_id.department_id.name) + " at " + str(
                fields.datetime.now())
            rec.confirm_pre_costing = temp
            rec.state = 'confirm'
            return

    def action_cancel(self):
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
        if vals.get('eem_sequence', _('Draft')) == _('Draft'):
            vals['eem_sequence'] = self.env['ir.sequence'].next_by_code('eem.pre_costing') or _(
                'Draft')  # sequence value
        res = super(EemPrecosting, self).create(vals)
        return res

    # Get automatic department after selecting employee
    @api.onchange('employee_id')
    def onchange_employee_id(self):
        if self.employee_id:
            if self.employee_id.department_id.name:
                self.expense_dept = self.employee_id.department_id.name
        else:
            self.expense_dept = ''


###### Notebook for Pre-costing ######
class EntertainmentPreCostingLine(models.Model):
    _name = "entertainment.pre_costing.line"
    _description = "Entertainment Pre-Costing Lines"

    entertainment_pre_costing_id = fields.Many2one('eem.pre_costing', string='Entertainment Pre-Costing:')
    product_id = fields.Many2one('eem.product', string='Product', domain=[('is_entertainment', '=', True)],
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


class ConveyancePreCostingLine(models.Model):
    _name = "conveyance.pre_costing.line"
    _description = "Conveyance Pre-Costing Lines"

    conveyance_pre_costing_id = fields.Many2one('eem.pre_costing', string='Conveyance Pre-Costing:')
    product_id = fields.Many2one('eem.product', string='Product', domain=[('is_conveyance', '=', True)],
                                 change_default=True, tracking=True)  # Category based product
    amount = fields.Float(string='Amount', tracking=True)
    remark = fields.Char(string='Remarks')


class MiscellaneousPreCostingLine(models.Model):
    _name = "miscellaneous.pre_costing.line"
    _description = "Miscellaneous Pre-Costing Lines"

    miscellaneous_pre_costing_id = fields.Many2one('eem.pre_costing', string='Miscellaneous Pre-Costing:')
    product_id = fields.Many2one('eem.product', string='Product', domain=[('is_miscellaneous', '=', True)],
                                 change_default=True, tracking=True)  # Category based product
    designation = fields.Char(string='Designation', required=True, tracking=True)
    amount = fields.Float(string='Amount', tracking=True)
    remark = fields.Char(string='Remarks')


class PurchasePreCostingLine(models.Model):
    _name = "purchase.pre_costing.line"
    _description = "Purchase Pre-Costing Lines"

    purchase_pre_costing_id = fields.Many2one('eem.pre_costing', string='Purchase Pre-Costing:')
    purchase_ref_no = fields.Char(string='Purchase Ref. No', tracking=True)
    amount = fields.Float(string='Amount', tracking=True)
    remark = fields.Char(string='Remarks')


class GiftDonationPreCostingLine(models.Model):
    _name = "gift_donation.pre_costing.line"
    _description = "Gift & Donation Pre-Costing Line"

    gift_donation_pre_costing_id = fields.Many2one('eem.pre_costing', string='Conveyance Pre-Costing:')
    product_id = fields.Many2one('eem.product', string='Service Name', domain=[('is_gift_donation', '=', True)],
                                 change_default=True, tracking=True)  # Category based product
    description = fields.Text(string='Description')
    amount = fields.Float(string='Amount')
    remark = fields.Char(string='Remarks')


class PrintingStationeryPreCostingLine(models.Model):
    _name = "printing_stationery.pre_costing.line"
    _description = "Printing & Stationery Pre-Costing Line"

    printing_stationery_pre_costing_id = fields.Many2one('eem.pre_costing', string='Conveyance Pre-Costing:')
    product_id = fields.Many2one('eem.product', string='Product Name', domain=[('is_printing_stationery', '=', True)],
                                 change_default=True, tracking=True)  # Category based product
    description = fields.Text(string='Description')
    amount = fields.Float(string='Amount')
    remark = fields.Char(string='Remarks')
