# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class CreateAppointmentWizard(models.TransientModel):
    _name = "create.appointment.wizard"
    _description = "Create Appointment Wizard"

    # Default_get Function for active id
    @api.model
    def default_get(self, fields):
        res = super(CreateAppointmentWizard, self).default_get(fields)
        if self._context.get('active_id'):
            res['patient_id'] = self._context.get('active_id')
        return res

    patient_id = fields.Many2one('hospital.patient', string='Patient Name:', required=True)  # override_field
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor Name:', required=True) # override_field
    reference = fields.Char(string='Reference :')
    date_appointment = fields.Date(string='Appointment Date :', required=False)
    age = fields.Integer(string='Age:')

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            if self.patient_id.age:
                self.age = self.patient_id.age
            if self.patient_id.sequence_no:
                self.reference = self.patient_id.sequence_no

    def action_create_appointment(self):
        vals = {
            'patient_id': self.patient_id.id,
            'age': self.patient_id.age,
            'reference': self.patient_id.sequence_no,
            'date_appointment': self.date_appointment
        }
        appointment_rec = self.env['hospital.appointment'].create(vals)
        return {
            'name': _('Appointment'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hospital.appointment',
            'res_id': appointment_rec.id,
            # 'target' : 'new',
        }
