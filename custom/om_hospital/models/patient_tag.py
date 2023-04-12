from odoo import api, fields, models
from datetime import date


class PatientTag(models.Model):
    _name = "patient.tag"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Patient Tag"

    name = fields.Char(string='name', required=True)
    active = fields.Boolean(default=True, string='Active')
    color = fields.Integer(string='color')
    color_2 = fields.Char(string='color 2')
