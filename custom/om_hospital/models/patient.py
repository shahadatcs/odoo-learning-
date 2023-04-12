from odoo import api, fields, models
from datetime import date


# create a database table
class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"

    name = fields.Char(string='Name', tracking=True)  # tracking name, age, gender
    date_of_birth = fields.Date(string='Date of Birth')
    ref = fields.Char(string='reference')
    age = fields.Integer(string='Age', compute='calculate_age', tracking=True)
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('kids', 'Kids'), ('neuter', 'Neuter'), ('common', 'Common'),
         ('other', 'Other')], string='Gender', tracking=True, default='other')
    active = fields.Boolean(default=True, string='True')
    image = fields.Image(string='image')
    tag_ids = fields.Many2many('patient.tag', string='tags')

    # Create Computed Field
    @api.depends('date_of_birth')
    def calculate_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 1



