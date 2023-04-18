from odoo import api, fields, models
from datetime import date


# create a database table
class HospitalPatientTest(models.Model):
    _name = "hospital.patient.test"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient Test"

    name = fields.Char(string='Name', tracking=True)  # tracking name, age, gender
