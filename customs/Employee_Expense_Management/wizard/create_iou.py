# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class CreateIOUWizard(models.TransientModel):
    _name = "create.iou.wizard"
    _description = "Create IOU Wizard"

    # Default_get Function for active id
    @api.model
    def default_get(self, fields):
        res = super(CreateIOUWizard, self).default_get(fields)
        if self._context.get('active_id'):
            res['ebm_sequence_id'] = self._context.get('active_id')
        return res

    ebm_sequence_id = fields.Many2one('ebm.management', string='Reference:', required=True)  # override_field
    employee_id = fields.Many2one('hr.employee', string='Employee :')
    expense_dept = fields.Char(string='Exp Department :')
    ebm_date = fields.Datetime(string='EBM Create Date :', readonly=True)
    required_date = fields.Date(string='Required Date :', required=True, tracking=True)
    requested_amount = fields.Integer(string='Requested Amount : ', tracking=True)
    purpose = fields.Text(string='Purpose :', required=True, tracking=True)

    @api.onchange('ebm_sequence_id')
    def onchange_ebm_sequence_id(self):
        if self.ebm_sequence_id:
            if self.ebm_sequence_id.employee_id:
                self.employee_id = self.ebm_sequence_id.employee_id
            if self.ebm_sequence_id.expense_dept:
                self.expense_dept = self.ebm_sequence_id.expense_dept
            if self.ebm_sequence_id.ebm_date:
                self.ebm_date = self.ebm_sequence_id.ebm_date
            if self.ebm_sequence_id.required_date:
                self.required_date = self.ebm_sequence_id.required_date
            if self.ebm_sequence_id.total_pre_costing_amount:
                self.requested_amount = self.ebm_sequence_id.total_pre_costing_amount
            if self.ebm_sequence_id.purpose:
                self.purpose = self.ebm_sequence_id.purpose

    def action_create_iou(self):
        vals = {
            'reference': self.ebm_sequence_id.ebm_sequence,
            'employee_id': self.ebm_sequence_id.employee_id.id,
            'expense_dept': self.ebm_sequence_id.expense_dept,
            'iou_date': self.ebm_sequence_id.ebm_date,
            'required_date': self.ebm_sequence_id.required_date,
            'requested_amount': self.ebm_sequence_id.total_pre_costing_amount,
            'purpose': self.ebm_sequence_id.purpose,

        }
        iou_rec = self.env['iou.management'].create(vals)
        return {
            'name': _('IOU'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'iou.management',
            'res_id': iou_rec.id,
            # 'target' : 'new',
        }
