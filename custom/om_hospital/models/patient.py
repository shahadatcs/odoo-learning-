from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import ValidationError


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
    #  appointment_id = fields.Many2one('hospital.appointment', string='Appointments')
    image = fields.Image(string='image')
    tag_ids = fields.Many2many('patient.tag', string='tags')
    appointment_count = fields.Integer(string='Appointment Count')

    # @api.model
    # def create(self, vals):
    #     print('Odoo mates', vals)
    #     vals['ref'] = 'OMTEST'
    #     return super(HospitalPatient, self).create(vals)

    # Python constraints
    # @api.constrains('date_of_birth')
    # def _check_date_of_birth(self):
    #     for rec in self:
    #         if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
    #             raise ValidationError(_('The entered data date_of_birth is not acceptable '))

    @api.model
    def create(self, vals):
        print('Odoo mates', vals)
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).create(vals)

    @api.model
    def writ(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).writ(vals)

    def name_get(self):
        patient_list = []

        for record in self:
            name = record.ref + ' ' + record.name
            patient_list.append((record.id, name))
            return patient_list
            # return [(record.id, "[%s] %s", (record.id, name)) for record in self:]

    # Create Computed Field
    @api.depends('date_of_birth')
    def calculate_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 1
