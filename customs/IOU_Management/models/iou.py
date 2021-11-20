from datetime import datetime

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class IouManagement(models.Model):
    _name = "iou.management"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Iou Management"

    iou_no = fields.Char(string='IOU No :', required=True, copy=False, readonly=True, default=lambda
        self: _('New'))  # sequence_id
    name = fields.Many2one('hr.employee', string='Created By :', default=lambda self: self.env.user.employee_id,
                           readonly=True)
    dept = fields.Many2one('hr.department', string='Department :', default=lambda self: self.env.user.department_id,
                           readonly=True)
    # expense_dept_for = fields.Selection([
    #     ('own', 'Own'),
    #     ('other', 'Other'),
    # ], string='Expense For :',  default='own', tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Employee :', default=lambda self: self.env.user.employee_id,
                                  tracking=True)
    expense_dept = fields.Char(string='Exp Department :')

    iou_date = fields.Datetime(string='IOU Date :', default=datetime.today(), readonly=True)
    required_date = fields.Date(string='Required Date :', required=True, tracking=True)

    reference = fields.Char(string='Reference :', required=True, tracking=True)
    requested_amount = fields.Integer(string='Requested Amount : ', required=True, tracking=True)
    purpose = fields.Text(string='Purpose :', required=True, tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('iou_no', _('New')) == _('New'):  # sequence value
            vals['iou_no'] = self.env['ir.sequence'].next_by_code('iou.management') or _(
                'New')  # sequence value
        res = super(IouManagement, self).create(vals)
        return res

    # force somethings to fillup before creating and editing the record
    # field validation
    @api.constrains('requested_amount')
    def check_requested_amount(self):
        for rec in self:
            if rec.requested_amount == 0:
                raise ValidationError(
                    _("Please Enter Correct Amount !!  Amount can not be Zero !! দয়া করে সঠিক পরিমাণ লিখুন !!"))

    # Date field validation
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
