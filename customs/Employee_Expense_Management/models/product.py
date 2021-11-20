from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EbmProduct(models.Model):
    _name = "ebm.product"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Ebm Management Product"

    name = fields.Char(string='Product Name :', required=True, tracking=True)
    product_img = fields.Binary(string='Image', tracking=True)
    is_entertainment = fields.Boolean(string='Is Entertainment :', default=False, tracking=True)
    is_conveyance = fields.Boolean(string='Is Conveyance :', default=False, tracking=True)
    is_miscellaneous = fields.Boolean(string='Is Miscellaneous :', default=False, tracking=True)
    unit_cost = fields.Float(string='Cost', tracking=True)
    note = fields.Text(string='Note : ', tracking=True)

    # field validation
    # @api.constrains('unit_cost')
    # def check_unit_cost(self):
    #     for rec in self:
    #         if rec.unit_cost == 0:
    #             raise ValidationError(
    #                 _("Please Enter Correct Amount. Amount can not be Zero !!\n ---- দয়া করে সঠিক পরিমাণ লিখুন "
    #                   "----!"))
