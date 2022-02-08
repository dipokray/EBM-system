from odoo import fields, models, api


class DynamicFieldBank(models.Model):
    _name = 'dynamic.field'
    _description = "Dynamic Product and other value"
    _rec_name = 'dynamic_for_bank'

    # dynamic_for_bank = fields.Char(string="Bank Expense Product", required=False)
    dynamic_for_bank = fields.Selection(string="", selection=[('conveyance', '1. Conveyance'),
                                                              ('entertainment', '2. Entertainment'),
                                                              ('print', '3. Print'),
                                                              ('bank_commission', '4. Bank commission'),
                                                              ('swift_charge', '5. Swift charge'),
                                                              ('vat_on_swift_charge', '6. Vat On Swift Charge'),
                                                              ('vat_mergin', '7. Vat On Mergin'),
                                                              ('lc_appli_charge', '8. L/C Application form Charge'),
                                                              ('lcaf_charge', '9. LCAF form Charge'),
                                                              ('amendment_charge', '10. Amendment Charge'), (
                                                                  'swift_amendment_charge',
                                                                  '11. Swift on Amendment Charge'), (
                                                                  'shipping_gurantee_charge',
                                                                  '12. Shipping GuranteeCharge'),
                                                              ('vat_ship_gurantee', '13. VAT on shipping gurantee'),
                                                              ('stamp', '14. Stamp')], required=True,
                                        track_visibility="always")
    conf_bank = fields.Float(string="Bank", required=False, )
    conf_cash = fields.Float(string="Cash", required=False, )


class DynamicFieldDocuments(models.Model):
    _name = 'dynamic.importdocuments'
    _description = "Dynamic Product and other value"
    _rec_name = 'dynamic_for_documents'

    # dynamic_for_documents = fields.Char(string=" Documets List", required=False)
    dynamic_for_documents = fields.Selection(string="Import document Expense",
                                             selection=[('awb_charge', '1. AWB Charge'),
                                                        ('misc', '2. Misc Incorrect Document'), (
                                                            'misc_bag_wallet',
                                                            '3. Misc Bag or wallet receive with import materials'),
                                                        ('misc_awb_copy', '4. Misc Problem in AWB copy'),
                                                        (
                                                            'misc_warehouse_security',
                                                            '5. Misc Import Warehouse security'),
                                                        ('print', '6. Print Or Photocopy')], required=True, )
    conf_doc_bank = fields.Float(string="Bank", required=False, )
    conf_doc_cash = fields.Float(string="Cash", required=False, )


class DynamicFieldtransportation(models.Model):
    _name = 'dynamic.importtransportation'
    _description = "Dynamic Product and other value"
    _rec_name = 'dynamic_for_transportation'

    # dynamic_for_transportation = fields.Char(string=" Transportation List", required=False)
    dynamic_for_transportation = fields.Selection(string="Transportation Cost",
                                                  selection=[('1. Carriage_Inwards', '1. Carriage Inwards'),
                                                             ('2. Driver_Boksis', '2. Driver Boksis'), ],
                                                  required=True, )
    conf_transport_bank = fields.Float(string="Bank", required=False, )
    conf_transport_cash = fields.Float(string="Cash", required=False, )


class DynamicFieldCnf(models.Model):
    _name = 'dynamic.importcnf'
    _description = "Dynamic Product and other value"
    _rec_name = 'dynamic_for_cnf'

    # dynamic_for_cnf = fields.Char(string=" CNF List", required=False)
    dynamic_for_cnf = fields.Selection(string="C & f Cost", selection=[('1. CNF_bill', '1. C & f Bill')],
                                       required=True, )
    conf_cnf_bank = fields.Float(string="Bank", required=False, )
    conf_cnf_cash = fields.Float(string="Cash", required=False, )


class DynamicFieldForwarder(models.Model):
    _name = 'dynamic.importforwarder'
    _description = "Dynamic Product and other value"
    _rec_name = 'dynamic_for_forwarder'

    # dynamic_for_forwarder = fields.Char(string=" Forwarder List", required=False)
    dynamic_for_forwarder = fields.Selection(string="Forwarder Cost",
                                             selection=[('1. Forwarder_Bill', '1. Forwarder Bill')],
                                             required=True, )
    conf_forwarder_bank = fields.Float(string="Bank", required=False, )
    conf_forwarder_cash = fields.Float(string="Cash", required=False, )


class DynamicFieldCourier(models.Model):
    _name = 'dynamic.importcourier'
    _description = "Dynamic Product and other value"
    _rec_name = 'dynamic_for_courier'

    # dynamic_for_courier = fields.Char(string=" Courier List", required=False)
    dynamic_for_courier = fields.Selection(string="Courier Charge", selection=[('1. Courier_Bill', '1. Courier Bill')],
                                           required=True, )
    conf_courier_bank = fields.Float(string="Bank", required=False, )
    conf_courier_cash = fields.Float(string="Cash", required=False, )


class DynamicFieldInsurance(models.Model):
    _name = 'dynamic.importinsurance'
    _description = "Dynamic Product and other value"
    _rec_name = 'dynamic_for_insurance'

    # dynamic_for_insurance = fields.Char(string=" Insurance List", required=False)
    dynamic_for_insurance = fields.Selection(string="Insurance Expense ",
                                             selection=[('1. Insurance-amount', '1. Insurance Amount'),
                                                        ('1. Pay_order_charge', '1. Pay Order Charge')],
                                             required=True, )
    conf_insurance_bank = fields.Float(string="Bank", required=False, )
    conf_insurance_cash = fields.Float(string="Cash", required=False, )

    #################### Given below For Export model#############################


class ExpDynamicFieldBank(models.Model):
    _name = 'expdynamic.field'
    _description = "Dynamic Product and other value"
    _rec_name = 'dynamic_for_expbank'

    # dynamic_for_expbank = fields.Char(string="Bank Expense Product", required=False)
    dynamic_for_expbank = fields.Selection(string="", selection=[('conveyance', '1. Conveyance'),
                                                                 ('entertainment', '2. Entertainment'),
                                                                 ('print', '3. Print'),
                                                                 ('bank_charge_postage', '4. Bank Charge Postage'),
                                                                 (
                                                                     'bank_charge_commission',
                                                                     '5. Bank Charge Commission'),
                                                                 ('bank_vat_commission',
                                                                  '6. Bank Charge VAT on Commission'),
                                                                 ('source_tax_ait', '7. Source Tax AIT'),
                                                                 ], required=True, )
    conf_expo_bank = fields.Float(string="Bank", required=False, )
    conf_expo_cash = fields.Float(string="Cash", required=False, )


class ExpDynamicFieldDocuments(models.Model):
    _name = 'dynamic.expdocuments'
    _description = "Dynamic Product and other value"
    _rec_name = 'dynamic_for_expdocuments'

    # dynamic_for_expdocuments = fields.Char(string=" Documets List", required=False)
    dynamic_for_expdocuments = fields.Selection(string="Shipping document Expense",
                                                selection=[('gsp_co_purchase', '1. GSP CO Purchase'),
                                                           ('gsp_endorsement', '2. GSP Endorsement'), (
                                                               'gsp_issue',
                                                               '3. GSP Issue Misc'),
                                                           ('conveyance', '4. Conveyance'),
                                                           ('entertainment', '5. Entertainment'),
                                                           ('print', '6. Print Or Photocopy'),
                                                           ('export_certificate', '7. Export Certificate'),
                                                           ('stamp', '8. Stamp')], required=True, )
    conf_shipping_bank = fields.Float(string="Bank", required=False, )
    conf_shipping_cash = fields.Float(string="Cash", required=False, )


class ExpDynamicFieldtransportation(models.Model):
    _name = 'dynamic.exptransportation'
    _description = "Dynamic Product and other value"
    _rec_name = 'dynamic_for_exptransportation'

    # dynamic_for_exptransportation = fields.Char(string=" Transportation List", required=False)
    dynamic_for_exptransportation = fields.Selection(string="Transportation Cost",
                                                     selection=[('carriage_inwards', '1. Carriage Inwards'),
                                                                ('parking_fee', '2. Toll or Parking fees'), ],
                                                     required=True, )

    conf_expo_transport_bank = fields.Float(string="Bank", required=False, )
    conf_expo_transport_cash = fields.Float(string="Cash", required=False, )


class ExpDynamicFieldCnf(models.Model):
    _name = 'dynamic.expcnf'
    _description = "Dynamic Product and other value"
    _rec_name = 'dynamic_for_expcnf'

    # dynamic_for_expcnf = fields.Char(string=" CNF List", required=False)
    dynamic_for_expcnf = fields.Selection(string="C & f Cost", selection=[('cnf_bill', 'C & f Bill')],
                                          required=True, )
    conf_expo_cnf_bank = fields.Float(string="Bank", required=False, )
    conf_expo_cnf_cash = fields.Float(string="Cash", required=False, )


class ExpDynamicFieldForwarder(models.Model):
    _name = 'dynamic.expforwarder'
    _description = "Dynamic Product and other value"
    _rec_name = 'dynamic_for_expforwarder'

    # dynamic_for_expforwarder = fields.Char(string=" Forwarder List", required=False)
    dynamic_for_expforwarder = fields.Selection(string="Forwarder Cost",
                                                selection=[('forwarder_bill', 'Forwarder Bill')],
                                                required=True, )
    conf_expo_forwarder_bank = fields.Float(string="Bank", required=False, )
    conf_expo_forwarder_cash = fields.Float(string="Cash", required=False, )


class ExpDynamicFieldCourier(models.Model):
    _name = 'dynamic.expcourier'
    _description = "Dynamic Product and other value"
    _rec_name = 'dynamic_for_expcourier'

    # dynamic_for_expcourier = fields.Char(string=" Courier List", required=False)
    dynamic_for_expcourier = fields.Selection(string="Courier Charge", selection=[('courier_bill', 'Courier Bill')],
                                              required=True, )
    conf_expo_courier_bank = fields.Float(string="Bank", required=False, )
    conf_expo_courier_cash = fields.Float(string="Cash", required=False, )
