# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"
    _order = "sequence_no desc"  # For ordering asc or dsc in tree view

    # Default_get Function
    @api.model
    def default_get(self, fields):
        res = super(HospitalPatient, self).default_get(fields)
        res['gender'] = 'male'
        # res['age'] = '18'
        res['note'] = 'New Patient'
        return res

    sequence_no = fields.Char(string='Patient ID', required=True, copy=False, readonly=True, default=lambda
        self: _('New'))  # sequence_id
    name = fields.Char(string='Name', required=True, tracking=True)
    age = fields.Integer(string='Age', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male', tracking=True)
    phone = fields.Char(string='Phone', tracking=True)
    note = fields.Text(string='Description', tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('done', 'Done'), ('cancel', 'Canceled')], default='draft', string="Status",
                             tracking=True)
    # override_field
    responsible_id = fields.Many2one('res.partner', string='Responsible', tracking=True)
    appointment_count = fields.Integer(string='Total Appointment', compute='_compute_appointment_count')
    patient_img = fields.Binary(string='Image')

    # notebook  override
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Appointments')

    # Count Function
    # Search Method
    def _compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            rec.appointment_count = appointment_count

    # Status Bar Button Action

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    # Sequence Value
    # Create method
    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = "New Patient"
        if vals.get('sequence_no', _('New')) == _('New'):  # sequence value
            vals['sequence_no'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')  # sequence value
        res = super(HospitalPatient, self).create(vals)
        return res

    # duplicate name  can't use function'

    @api.constrains('name')
    def check_name(self):
        for rec in self:  # For avoiding singleton error
            patients = self.env['hospital.patient'].search([('name', '=', rec.name), ('id', '!=', rec.id)])
            if patients:
                raise ValidationError(_("Name %s already Exists !!." % rec.name))

    # force somethings to fillup before creating and editing the record
    # field validation
    @api.constrains('age', 'phone')
    def check_age(self):
        for rec in self:
            if rec.age == 0:
                raise ValidationError(_("Please Enter Age !!  Age can not be Zero !!"))
            if rec.phone == 0:
                raise ValidationError(_("Please Enter Phone Number !! Phone number can not be empty !!"))

    # default name,id , gender get function in same line
    @api.model
    def name_get(self):
        res = []  # Empty list that can store the list data
        for rec in self:
            # res.append((rec.id, '%s - %s ' % (rec.sequence_no, rec.name)))
            # Method:2
            name = rec.sequence_no + '--' + rec.name
            res.append((rec.id, name))
        return res

    # Name_search method based on searching by id or name
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        domain = args + ['|', ('sequence_no', operator, name), ('name', operator, name)]
        return super(HospitalPatient, self).search(domain, limit=limit).name_get()

    # Smart Appointment button action for view
    def action_open_appointments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'hospital.appointment',
            'view_type': 'form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},  # for get active id
            'view_mode': 'tree,form',
            'target': 'current',
        }
