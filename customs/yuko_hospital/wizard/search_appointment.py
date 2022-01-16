# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class SearchAppointmentWizard(models.TransientModel):
    _name = "search.appointment.wizard"
    _description = "Search Appointment Wizard"

    patient_id = fields.Many2one('hospital.patient', string='Patient :', required=True)  # override_fleld

    # Method 1
    def action_search_appointment(self):
        action = self.env.ref('yuko_hospital.action_hospital_appointment').read()[0]
        action['domain'] = [('patient_id', '=', self.patient_id.id)]
        return action

    #    # Method 2
    # def action_search_appointment(self):
    #     action = self.env['ir.actions.actions']._for_xml_id(
    #         'yuko_hospital.action_hospital_appointment')  # For_View _Appointment
    #     action['domain'] = [('patient_id', '=', self.patient_id.id)]  # For selected patient
    #     return action
    #
    # # Method 3
    # def action_search_appointment(self):
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Appointments',
    #         'res_model': 'hospital.appointment',
    #         'view_type': 'form',
    #         'domain': [('patient_id', '=', self.patient_id.id)],
    #         'view_mode': 'tree,form',
    #         'target': 'current',
    #     }


