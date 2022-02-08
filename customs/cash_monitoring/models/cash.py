from odoo import api, models, fields


class CashBalance(models.Model):
    _name = 'cashbalance.cashbalance'
    _description = 'Cash Balance'

    atk = fields.Integer('TK.1000')
    btk = fields.Integer('TK.500')
    ctk = fields.Integer('TK.100')
    dtk = fields.Integer('TK.50')
    etk = fields.Integer('TK.20')
    ftk = fields.Integer('TK.10')
    gtk = fields.Integer('TK.5')
    htk = fields.Integer('TK.2')
    date = fields.Date(required=True, default=fields.Date.context_today)
    total = fields.Integer('Total Entry', compute='_compute_amount', store=True)
    cash = fields.Integer('Total Cash-In', compute='get_data', store=True)

    sum_atk = fields.Integer('Quantity of 1000.TK', compute='get_atk', store=True)
    totalatk = fields.Integer(compute='total_atk', store=True)

    sum_btk = fields.Integer('Quantity of  500.TK', compute='get_btk', store=True)
    totalbtk = fields.Integer(compute='total_btk', store=True)

    sum_ctk = fields.Integer('Quantity of  100.TK', compute='get_ctk', store=True)
    totalctk = fields.Integer(compute='total_ctk', store=True)

    sum_dtk = fields.Integer('Quantity of  50.TK', compute='get_dtk', store=True)
    totaldtk = fields.Integer(compute='total_dtk', store=True)

    sum_etk = fields.Integer('Quantity of  20.TK', compute='get_etk', store=True)
    totaletk = fields.Integer(compute='total_etk', store=True)

    sum_ftk = fields.Integer('Quantity of  10.TK', compute='get_ftk', store=True)
    totalftk = fields.Integer(compute='total_ftk', store=True)

    sum_gtk = fields.Integer('Quantity of  5.TK', compute='get_gtk', store=True)
    totalgtk = fields.Integer(compute='total_gtk', store=True)

    sum_htk = fields.Integer('Quantity of   2.TK', compute='get_htk', store=True)
    totalhtk = fields.Integer(compute='total_htk', store=True)

    @api.depends('atk', 'btk', 'ctk', 'dtk', 'etk', 'ftk', 'gtk', 'htk')
    def _compute_amount(self):
        for expense in self:
            expense.total = expense.atk * 1000 + expense.btk * 500 + expense.ctk * 100 + expense.dtk * 50 \
                            + expense.etk * 20 + expense.ftk * 10 + expense.gtk * 5 + expense.htk * 2

    @api.depends('total')
    def get_data(self):
        for rec in self:
            if not isinstance(rec.id, models.NewId):
                cash = 0
                for cashin in self.search([('id', '<', rec.id)]):
                    cash += cashin.total
                cash += rec.total
                rec.cash = cash
        return True

    @api.depends('atk')
    def total_atk(self):
        for exp in self:
            exp.totalatk = exp.atk

    @api.depends('totalatk')
    def get_atk(self):
        for rec in self:
            if not isinstance(rec.id, models.NewId):
                sum_atk = 0
                for getatk in self.search([('id', '<', rec.id)]):
                    sum_atk += getatk.totalatk
                sum_atk += rec.totalatk
                rec.sum_atk = sum_atk
        return True

    @api.depends('btk')
    def total_btk(self):
        for exp in self:
            exp.totalbtk = exp.btk

    @api.depends('totalbtk')
    def get_btk(self):
        for rec in self:
            if not isinstance(rec.id, models.NewId):
                sum_btk = 0
                for getbtk in self.search([('id', '<', rec.id)]):
                    sum_btk += getbtk.totalbtk
                sum_btk += rec.totalbtk
                rec.sum_btk = sum_btk
        return True

    @api.depends('ctk')
    def total_ctk(self):
        for exp in self:
            exp.totalctk = exp.ctk

    @api.depends('totalctk')
    def get_ctk(self):
        for rec in self:
            if not isinstance(rec.id, models.NewId):
                sum_ctk = 0
                for getctk in self.search([('id', '<', rec.id)]):
                    sum_ctk += getctk.totalctk
                sum_ctk += rec.totalctk
                rec.sum_ctk = sum_ctk
        return True

    @api.depends('dtk')
    def total_dtk(self):
        for exp in self:
            exp.totaldtk = exp.dtk

    @api.depends('totaldtk')
    def get_dtk(self):
        for rec in self:
            if not isinstance(rec.id, models.NewId):
                sum_dtk = 0
                for getdtk in self.search([('id', '<', rec.id)]):
                    sum_dtk += getdtk.totaldtk
                sum_dtk += rec.totaldtk
                rec.sum_dtk = sum_dtk
        return True

    @api.depends('etk')
    def total_etk(self):
        for exp in self:
            exp.totaletk = exp.etk

    @api.depends('totaletk')
    def get_etk(self):
        for rec in self:
            if not isinstance(rec.id, models.NewId):
                sum_etk = 0
                for getetk in self.search([('id', '<', rec.id)]):
                    sum_etk += getetk.totaletk
                sum_etk += rec.totaletk
                rec.sum_etk = sum_etk
        return True

    @api.depends('ftk')
    def total_ftk(self):
        for exp in self:
            exp.totalftk = exp.ftk

    @api.depends('totalftk')
    def get_ftk(self):
        for rec in self:
            if not isinstance(rec.id, models.NewId):
                sum_ftk = 0
                for getftk in self.search([('id', '<', rec.id)]):
                    sum_ftk += getftk.totalftk
                sum_ftk += rec.totalftk
                rec.sum_ftk = sum_ftk
        return True

    @api.depends('gtk')
    def total_gtk(self):
        for exp in self:
            exp.totalgtk = exp.gtk

    @api.depends('totalgtk')
    def get_gtk(self):
        for rec in self:
            if not isinstance(rec.id, models.NewId):
                sum_gtk = 0
                for getgtk in self.search([('id', '<', rec.id)]):
                    sum_gtk += getgtk.totalgtk
                sum_gtk += rec.totalgtk
                rec.sum_gtk = sum_gtk
        return True

    @api.depends('htk')
    def total_htk(self):
        for exp in self:
            exp.totalhtk = exp.htk

    @api.depends('totalhtk')
    def get_htk(self):
        for rec in self:
            if not isinstance(rec.id, models.NewId):
                sum_htk = 0
                for gethtk in self.search([('id', '<', rec.id)]):
                    sum_htk += gethtk.totalhtk
                sum_htk += rec.totalhtk
                rec.sum_htk = sum_htk
        return True

    a = fields.Integer('TK.1000')
    b = fields.Integer('TK.500')
    c = fields.Integer('TK.100')
    d = fields.Integer('TK.50')
    e = fields.Integer('TK.20')
    f = fields.Integer('TK.10')
    g = fields.Integer('TK.5')
    h = fields.Integer('TK.2')

    dateo = fields.Date(required=True, default=fields.Date.context_today)
    amount = fields.Integer(' Total Entry', compute='compute_amount', store=True)
    cashout = fields.Integer('Total Cash-Out', compute='get_amount', store=True)

    sum_a = fields.Integer('Quantity of  1000.TK', compute='get_a', store=True)
    totala = fields.Integer(compute='total_a', store=True)
    # result_a = fields.Integer('1000.TK', compute='update_a', store=True)

    sum_b = fields.Integer('Quantity of  500.TK', compute='get_b', store=True)
    totalb = fields.Integer(compute='total_b', store=True)
    # result_b = fields.Integer(compute='Result_b', store=True)

    sum_c = fields.Integer('Quantity of  100.TK', compute='get_c', store=True)
    totalc = fields.Integer(compute='total_c', store=True)
    # result_c = fields.Integer(compute='Result_c', store=True)

    sum_d = fields.Integer('Quantity of  50.TK', compute='get_d', store=True)
    totald = fields.Integer(compute='total_d', store=True)
    # result_d = fields.Integer(compute='Result_d', store=True)

    sum_e = fields.Integer('Quantity of  20.TK', compute='get_e', store=True)
    totale = fields.Integer(compute='total_e', store=True)
    # result_e = fields.Integer(compute='Result_e', store=True)

    sum_f = fields.Integer('Quantity of  10.TK', compute='get_f', store=True)
    totalf = fields.Integer(compute='total_f', store=True)
    # result_f = fields.Integer(compute='Result_f', store=True)

    sum_g = fields.Integer('Quantity of  5.TK', compute='get_g', store=True)
    totalg = fields.Integer(compute='total_g', store=True)
    # result_g = fields.Integer(compute='Result_g', store=True)

    sum_h = fields.Integer('Quantity of   2.TK', compute='get_h', store=True)
    totalh = fields.Integer(compute='total_h', store=True)
    # result_h = fields.Integer(compute='Result_h', store=True)

    Balance = fields.Integer('Total Cash Balance',compute='get_cash', store=True)

    @api.depends('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
    def compute_amount(self):
        for expense in self:
            expense.amount = expense.a * 1000 + expense.b * 500 + expense.c * 100 + expense.d * 50 \
                             + expense.e * 20 + expense.f * 10 + expense.g * 5 + expense.h * 2

    @api.depends('amount')
    def get_amount(self):
        for rec in self:
            if not isinstance(rec.id, models.NewId):
                cashout = 0
                for cash in self.search([('id', '<', rec.id)]):
                    cashout += cash.amount
                cashout += rec.amount
                rec.cashout = cashout
        return True

    #
    # @api.depends('cash')
    # def balance(self):
    #     data = self.env['cashinbalance.cashinbalance'].search(['cash'])

    @api.depends('a')
    def total_a(self):
        for exp in self:
            exp.totala = exp.a

    @api.depends('totala')
    def get_a(self):
        for rec in self:
            if not isinstance(rec.id, models.NewId):
                sum_a = 0
                for geta in self.search([('id', '<', rec.id)]):
                    sum_a += geta.totala
                sum_a += rec.totala
                rec.sum_a = sum_a
        return True

    @api.depends('b')
    def total_b(self):
        for exp in self:
            exp.totalb = exp.b

    @api.depends('totalb')
    def get_b(self):
        for rec in self:
            if not isinstance(rec.id, models.NewId):
                sum_b = 0
                for getb in self.search([('id', '<', rec.id)]):
                    sum_b += getb.totalb
                sum_b += rec.totalb
                rec.sum_b = sum_b
        return True

    @api.depends('c')
    def total_c(self):
        for exp in self:
            exp.totalc = exp.c

    @api.depends('totalc')
    def get_c(self):
        for rec in self:
            if not isinstance(rec.id, models.NewId):
                sum_c = 0
                for getc in self.search([('id', '<', rec.id)]):
                    sum_c += getc.totalc
                sum_c += rec.totalc
                rec.sum_c = sum_c
        return True

    @api.depends('d')
    def total_d(self):
        for exp in self:
            exp.totald = exp.d

    @api.depends('totald')
    def get_d(self):
        for rec in self:
            if not isinstance(rec.id, models.NewId):
                sum_d = 0
                for getd in self.search([('id', '<', rec.id)]):
                    sum_d += getd.totald
                sum_d += rec.totald
                rec.sum_d = sum_d
        return True

    @api.depends('e')
    def total_e(self):
        for exp in self:
            exp.totale = exp.e

    @api.depends('totale')
    def get_e(self):
        for rec in self:
            if not isinstance(rec.id, models.NewId):
                sum_e = 0
                for gete in self.search([('id', '<', rec.id)]):
                    sum_e += gete.totale
                sum_e += rec.totale
                rec.sum_e = sum_e
        return True

    @api.depends('f')
    def total_f(self):
        for exp in self:
            exp.totalf = exp.f

    @api.depends('totalf')
    def get_f(self):
        for rec in self:
            if not isinstance(rec.id, models.NewId):
                sum_f = 0
                for getf in self.search([('id', '<', rec.id)]):
                    sum_f += getf.totalf
                sum_f += rec.totalf
                rec.sum_f = sum_f
        return True

    @api.depends('g')
    def total_g(self):
        for exp in self:
            exp.totalg = exp.g

    @api.depends('totalg')
    def get_g(self):
        for rec in self:
            if not isinstance(rec.id, models.NewId):
                sum_g = 0
                for getg in self.search([('id', '<', rec.id)]):
                    sum_g += getg.totalg
                sum_g += rec.totalg
                rec.sum_g = sum_g
        return True

    @api.depends('h')
    def total_h(self):
        for exp in self:
            exp.totalh = exp.h

    @api.depends('totalh')
    def get_h(self):
        for rec in self:
            if not isinstance(rec.id, models.NewId):
                sum_h = 0
                for geth in self.search([('id', '<', rec.id)]):
                    sum_h += geth.totalh
                sum_h += rec.totalh
                rec.sum_h = sum_h
        return True

    @api.depends('cash', 'cashout')
    def get_cash(self):
        for rec in self:
            rec.Balance = rec.cash - rec.cashout
    #
    # @api.depends('sum_atk', 'sum_a')
    # def update_a(self):
    #     for rec in self:
    #         rec.result_a = rec.sum_atk - rec.sum_a
