# from datetime import datetime
#
# from odoo import fields, models, api
# from odoo.exceptions import ValidationError
#
#
# class Re_Visit(models.Model):
#     _name = 're.visit'
#     _inherit = ['mail.thread', 'mail.activity.mixin']
#     _description = 'Re-visitor '
#     _rec_name = 'v_name'
#     _order = 'check_in_date desc'
#
#     visitor_name = fields.Many2one('visitor.data', string='Search Your Name', required=True)
#     v_name = fields.Char(related='visitor_name.v_name', string="Name")
#     v_phn = fields.Integer(related='visitor_name.v_phn', string="Phone")
#     v_email = fields.Char(related='visitor_name.v_email', string="Email")
#     v_gender = fields.Selection(related='visitor_name.v_gender', string="Gender")
#     v_company = fields.Char(related='visitor_name.v_company', string='Company')
#     v_image = fields.Binary(related='visitor_name.v_image', string='Photo')
#     v_address = fields.Char(related='visitor_name.v_address', string='Address')
#
#     employee_id = fields.Many2one('hr.employee', string='Select Person', required=True)
#     image_1920 = fields.Image(related='employee_id.image_1920', string="Photo")
#     work_phone = fields.Char(related='employee_id.work_phone', string="Phone")
#     dept = fields.Many2one(related='employee_id.department_id', string="Department")
#     job_title = fields.Char(related='employee_id.job_title', string=" Job Position")
#     check_in_date = fields.Datetime(string='Check-In', default=datetime.today())
#     check_out_date = fields.Datetime(string='Check-Out')
#     appoint_count = fields.Integer(string='Appointment', computed='get_appoint_count')
