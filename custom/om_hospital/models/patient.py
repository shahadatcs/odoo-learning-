from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import ValidationError
from dateutil import relativedelta


# create a database table
class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"

    name = fields.Char(string='Name', tracking=True)  # tracking name, age, gender
    date_of_birth = fields.Date(string='Date of Birth')
    ref = fields.Char(string='reference')
    age = fields.Integer(string='Age', compute='calculate_age', inverse='_inverse_compute_age', search='_search_age',
                         tracking=True)
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('kids', 'Kids'), ('neuter', 'Neuter'), ('common', 'Common'),
         ('other', 'Other')], string='Gender', tracking=True, default='other')
    active = fields.Boolean(default=True, string='True')
    #  appointment_id = fields.Many2one('hospital.appointment', string='Appointments')
    image = fields.Image(string='image')
    tag_ids = fields.Many2many('patient.tag', string='tags')
    appointment_count = fields.Integer(string='Appointment Count', compute='count_appointment')
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")
    parent = fields.Char(string='Parent')
    marital_status = fields.Selection([('married', 'Married'), ('single', 'Single')], string='Marital Status',
                                      tracking=True)
    partner_name = fields.Char(string='Partner Name')
    is_birthday = fields.Boolean(string='Birthday ?', compute='compute_birthday')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    website = fields.Char(string='Website')

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

    @api.ondelete(at_uninstall=False)
    def _check_appointments(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(_('You cannot delete patient with appointment'))

    @api.depends('appointment_ids')
    def count_appointment(self):
        # for rec in self:
        appointment_group = self.env['hospital.appointment'].read_group(domain=[], fields=['patient_id'],
                                                                        groupby=['patient_id'])
        # print('Appointment', appointment_group)
        # for appointment in appointment_group:
        #     print('Appointment', appointment.get('patient_id')[0])
        #     patient_id = appointment.get('patient_id')[0]
        #     patient_rec = self.browse(patient_id)
        #     patient_rec.appointment_count = appointment['patient_id_count']
        #     self -= patient_rec
        self.appointment_count = 0

    # count appointment
    # rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])

    @api.model
    def create(self, vals):
        print('Odoo mates', vals)
        # Create sequnce
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).create(vals)

    @api.model
    def writ(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).writ(vals)

    # def name_get(self):
    #     patient_list = []
    #     for record in self:
    #         name = record.ref + ' ' + record.name
    #         patient_list.append((record.id, name))
    #     return patient_list

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

    # Inverse function for age calculation
    @api.depends('age')
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)
        return

    # @api.depends('age')
    def _search_age(self, operator, value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        start_of_year = date_of_birth.replace(day=1, month=1)
        end_of_year = date_of_birth.replace(day=31, month=12)
        return [('date_of_birth', '>=', start_of_year), ('date_of_birth', '>=', end_of_year)]

    def action_tet(self):
        print('Clicked')
        return

    @api.depends('date_of_birth')
    def compute_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.date_of_birth:
                today = date.today()
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    is_birthday = True
            rec.is_birthday = is_birthday

    def action_view_appointments(self):
        return {
            'name': _('Appointment'),
            'res_model': 'hospital.appointment',
            'view_mode': 'tree,form,calendar,activity',
            'context': {'default_patient_id': self.id},
            'domain': [('patient_id', '=', self.id)],
            'target': 'current',
            'type': 'ir.actions.act_window',
        }
