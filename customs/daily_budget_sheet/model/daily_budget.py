from odoo import api, fields, models, _
from datetime import datetime


# Database of entry intent form
class Daily_budget(models.Model):
	_name = 'dailybudget.new'
	_inherit = ['mail.thread', 'mail.activity.mixin']
	
	_description = 'Entry indent form'
	_rec_name = 'Indent_No'
	
	today_date_time = fields.Datetime(string='Indent Date and time', default=datetime.today(), readonly="True")
	
	reference = fields.Char(string="Reference")
	Indent_No = fields.Many2one('hr.employee', string="Indentor Department")
	
	indentor = fields.Char("Indentor", default=lambda self: self.env.user.name, readonly="True")
	
	indent_for = fields.Selection(string="Indent For", selection=
	[('I', 'Store'), ('J', 'MD-Sir Room'), ('K', 'Accounts & Finance'), ('L', 'Commercial(Export)'),
	 ('M', 'Commercial(Import)'), ('N', 'Commercial(Bond)'), ('O', 'HR & Admin'), ('P', 'CEO Sir')], required=True)
	
	particular = fields.Text(string="Purpose",
	                         help="Example : Note, Description ,Buyer Ref, Style, Buyer Order no, PI, PO etc.")
	
	Priority = fields.Selection(string="Priority", selection=[('T', 'Emergency'), ('U', 'Normal')],
	                            required=True)
	required_Data_time = fields.Date(string="Required Date", required=True)
	
	name_seq = fields.Char(string='Daily Budget Reference', required=True, copy=False, readonly=True,
	                       index=True, default=lambda self: _('New'))
	roni = fields.One2many('product.line', 'appointment_id', copy=True)
	
	# hr_dep = fields.One2many('hr.department', 'name', copy=True)
	
	@api.depends('roni', 'roni.actual_total')
	def compute_actual_total(self):
		for rec in self:
			total = 0
			for i in rec.roni:
				total += i.actual_total
			rec['total_amount'] = total
	
	currency_id = fields.Many2one('res.currency', string='Currency', readonly=True,
	                              default=lambda self: self.env.company.currency_id)
	total_amount = fields.Monetary('Total Amount', compute="compute_actual_total", store=True)
	
	def get_data(self):
		self.env.cr.execute("select indentor from dailybudget_new")
		self.env.cr.fetchall()
		for rec in self:
			print("Name", rec.indentor)
	
	state = fields.Selection([
		('draft', 'Draft'),
		('department', 'Department Manager'),
		('audit', 'Audit'),
		('management', 'Management'),
		('accounts', 'Accounts'),
		('paid', 'Paid')
	], string='Status', readonly=True, default='draft')
	
	def action_submit_to_manager(self):
		for rec in self:
			rec.state = 'department'
	
	def action_done(self):
		for rec in self:
			rec.state = 'done'
	
	def action_reset_to_draft(self):
		for rec in self:
			rec.state = 'draft'
	
	def action_approve_department_manager(self):
		
		for rec in self:
			rec.state = 'audit'
		# self.env.user.notify_success('Aprroved')
	
	def action_approve_audit(self):
		
		for rec in self:
			rec.state = 'management'
		# self.env.user.notify_success('Aprroved')
	
	#
	def action_approve_management(self):
		
		for rec in self:
			rec.state = 'accounts'
			# notification = {
			# 	'type': 'ir.actions.client',
			# 	'tag': 'display_notification',
			# 	'rec.state': 'accounts',
			# 	'params': {
			# 		'title': ('Your Custom Title'),
			# 		'message': 'Approved',
			# 		'type': 'success',  # types: success,warning,danger,info
			# 		'sticky': True,  # True/False will display for few seconds if false
			# 	},
			# }
			# return notification
	
	def action_approve_accounts(self):
		
		for rec in self:
			rec.state = 'paid'
		# self.env.user.notify_success('Aprroved')
	
	# inherit data from entry intent database through API
	@api.model
	def create(self, vals):
		if vals.get('name_seq', _('New')) == _('New'):
			vals['name_seq'] = self.env['ir.sequence'].next_by_code('daily.budget') or _('New')
		res = super(Daily_budget, self).create(vals)
		return res


class productline(models.Model):
	_name = 'product.line'
	# name = fields.Char(required=True)
	# display_type = fields.Selection([
	# 	('line_section', "Section"),
	# 	('line_note', "Note")], default=False, help="Technical field for UX purpose.")
	product_id = fields.Many2one('product.product', string='product')
	
	product_qty = fields.Integer(string="Quantity")
	price = fields.Float(string="Price")
	
	Payment_type = fields.Selection(string="Payment Type", selection=[('Q', 'Cash'), ('R', 'CHQ'), ('S', 'bkash')],
	                                required=True)
	expected_total = fields.Float(string="Expected Total", compute='count')
	
	actual_total = fields.Float(string="Actual Total")
	
	excess_amount = fields.Float(string="Excess amount", compute='difference_excess_amount')
	return_amount = fields.Float(string="Return amount", compute='difference_return_amount')
	remarks = fields.Text(string='Remarks')
	
	appointment_id = fields.Many2one('dailybudget.new', string='Appointment ID')
	
	def count(self):
		for rec in self:
			rec.expected_total = rec.product_qty * rec.price
	
	@api.depends('actual_total', 'expected_total')
	def difference_excess_amount(self):
		for rec in self:
			excess_amount = rec.actual_total - rec.expected_total
			rec.excess_amount = 0 if excess_amount < 0 else excess_amount
	
	@api.depends('actual_total', 'expected_total')
	def difference_return_amount(self):
		for rec in self:
			return_amount = rec.expected_total - rec.actual_total
			rec.return_amount = 0 if return_amount < 0 else return_amount
