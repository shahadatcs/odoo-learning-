# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PartnerCategory(models.Model):
    _name = 'res.partner.category'
    _inherit = ['res.partner.category', 'mail.thread']


    name = fields.Char(tracking = True)

