# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    so_confirmed_user_id = fields.Many2one('res.users', string='So Confirmed User')


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    line_number = fields.Integer(string='Line Number')
