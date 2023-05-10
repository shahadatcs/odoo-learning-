# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirmed_user_id = fields.Many2one('res.users', string='Confirmed User')

    def action_confirm(self):
        print('success..........')
        super(SaleOrder, self).action_confirm()
        self.confirmed_user_id = self.env.user.id

    def prepare_invoice(self):
        invoice_vals = super(SaleOrder, self).prepare_invoice()
        invoice_vals['so_confirmed_user_id'] = self.confirmed_user_id.id
        print('invoice_vals', invoice_vals)
        return invoice_vals
