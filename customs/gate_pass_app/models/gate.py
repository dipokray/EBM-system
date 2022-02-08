from odoo import tools
from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime


class Visitor(models.Model):
    _name = 'gate.data'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'gate data'
    _rec_name = 'employee_id'
    _order = 'out_time desc'

    user_id = fields.Many2one('res.users', string='User', track_visibility='onchange', readonly=True,
                              states={'draft': [('readonly', False)]}, default=lambda self: self.env.user)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    image_1920 = fields.Image(related='employee_id.image_1920', string="Photo")
    work_phone = fields.Char(related='employee_id.work_phone', string="Phone")
    work_email = fields.Char(related='employee_id.work_email', string="Email")
    dept = fields.Many2one(related='employee_id.department_id', string="Department")
    job_title = fields.Char(related='employee_id.job_title', string=" Job Position")

    check_in = fields.Datetime(string='Check-In')
    out_time = fields.Datetime(string='Out Time', default=fields.Datetime.now)
    expected_time = fields.Datetime(string='Expected Time')
    purpose = fields.Text(string="Purpose")
    destination = fields.Char(string="Destination")
    late_count = fields.Float(string='Late Hours', compute='late_calculate', store=True)
    # bonus_hour = fields.Float(string='Bonus Hour', compute='bonus_time_calculate', store=True)

    @api.depends('check_in', 'expected_time')
    def late_calculate(self):
        if self.check_in and self.expected_time:
            t1 = datetime.strptime(str(self.expected_time),'%Y-%m-%d %H:%M:%S')
            t2 = datetime.strptime(str(self.check_in),'%Y-%m-%d %H:%M:%S')
            t3 = t2 - t1
            tot_sec = t3.total_seconds()
            m = tot_sec / 3600
            # h = m / 60
            # duration_hour = float("%d.%d" % (h, m))
            self.late_count = float(m)






    # @api.depends('check_in', 'expected_time')
    # def bonus_time_calculate(self):
    #     if self.expected_time and self.check_in:
    #         t1 = datetime.strptime(str(self.expected_time), '%Y-%m-%d %H:%M:%S')
    #         t2 = datetime.strptime(str(self.check_in), '%Y-%m-%d %H:%M:%S')
    #         t3 = t1 - t2
    #         tot_sec = t3.total_seconds()
    #         m = tot_sec / 60
    #         h = m / 60
    #         duration_hour = ("%d.%d" % (h, m))
    #         self.bonus_hour = str(duration_hour)
# access_user,Access gate user,model_gate_data,group_gate_user,1,1,1,0
