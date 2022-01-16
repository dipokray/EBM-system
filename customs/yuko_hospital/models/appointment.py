# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"
    _order = "sequence_no desc"

    # _order = "doctor_id,sequence_no"  # add more fields

    sequence_no = fields.Char(string='Patient ID', copy=False, readonly=True, default=lambda
        self: _('New'))  # sequence_id
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True, tracking=True)  # override_field
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', tracking=True)  # override_field
    age = fields.Integer(string='Age', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], tracking=True)
    phone = fields.Char(string='Phone', tracking=True)
    reference = fields.Char(string='Reference :')

    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('done', 'Done'), ('cancel', 'Canceled')], default='draft', string="Status",
                             tracking=True)
    date_appointment = fields.Date(string='Date', tracking=True)
    appointment_time = fields.Datetime(string='Checkup Time', tracking=True)
    note = fields.Text(string='Description', tracking=True)
    # notebook fields
    prescription = fields.Text(string='Description', tracking=True)
    medicine = fields.Text(string='Medicine', tracking=True)

    # notebook line added field
    prescription_line_ids = fields.One2many('appointment.prescription.lines', 'appointment_id',
                                            string='Prescription  Lines')

    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = "New Patient"
        if vals.get('sequence_no', _('New')) == _('New'):  # sequence value
            vals['sequence_no'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _(
                'New')  # sequence value
        res = super(HospitalAppointment, self).create(vals)
        return res

    # Get all data of   any patient after selecting the patient
    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            if self.patient_id.age:
                self.age = self.patient_id.age
            if self.patient_id.gender:
                self.gender = self.patient_id.gender
            if self.patient_id.phone:
                self.phone = self.patient_id.phone
            if self.patient_id.note:
                self.note = self.patient_id.note

        # After removing the patient the filed will be empty
        else:
            self.age = ''
            self.gender = ''
            self.phone = ''
            self.note = ''

    # Delete or unlink method
    def unlink(self):
        if self.state == 'done':
            raise ValidationError(_("You can not delete %s as it is in Done state." % self.sequence_no))
        return super(HospitalAppointment, self).unlink()

    # Redirect another url function for new url link
    def action_url(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'https://www.linkedin.com/in/dipok-ray-053430144/',
            # For get dynamic url
            # 'url': 'https://apps.odoo.com/apps/modules/14.0/%s/' % self.prescription,
        }


# notebook model
class AppointmentPrescriptionLines(models.Model):
    _name = "appointment.prescription.lines"
    _description = "Appointment Prescription Lines"

    name = fields.Char(string="Medicine", required=True)
    qty = fields.Integer(string="Quantity")
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
