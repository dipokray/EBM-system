# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {'hospital.patient':'related_patient_id'}
    _description = "Hospital Doctor"

    # _rec_name = "doctor_name"

    # default name,id , gender get function in same line
    def name_get(self):
        result = []  # Empty list that can store the list data
        for rec in self:
            name = '[' + rec.reference + '] ' + rec.name
            result.append((rec.id, name))
        return result

    name = fields.Char(string='Name', required=True, tracking=True)
    reference = fields.Char(string='Doctor Reference', required=True, copy=False, readonly=True, default=lambda
        self: _('New'))  # sequence_id
    # patient_id = fields.Many2one('hospital.patient', string='Patient Name :')
    related_patient_id = fields.Many2one('hospital.patient', string='Patient Name :')
    age = fields.Integer(string='Age', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male', tracking=True)
    phone = fields.Char(string='Phone', tracking=True)
    note = fields.Text(string='Description', tracking=True)
    doctor_img = fields.Binary(string='Image')
    active = fields.Boolean(string="active", default="True")  # active or archived field
    appointment_count = fields.Integer(string='Total Appointment', compute='_compute_appointment_count')

    # Count Function
    def _compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('doctor_id', '=', rec.id)])
            rec.appointment_count = appointment_count

        # Sequence Value

    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):  # sequence value
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.doctor') or _('New')  # sequence value
        res = super(HospitalDoctor, self).create(vals)
        return res

    # duplicate .. default copy function
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _("%s (Copy)", self.name)
            default['age'] = ""
            default['phone'] = ""
            default['note'] = "Copied"

        return super(HospitalDoctor, self).copy(default)
