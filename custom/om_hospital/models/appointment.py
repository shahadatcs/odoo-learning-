from odoo import api, fields, models


# create a database table
class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"
    _rec_name = 'ref'

    patient_id = fields.Many2one(comodel_name='hospital.patient', string='patient')
    gender = fields.Selection(related='patient_id.gender')  # readonly=false that selection progress
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
    booking_date = fields.Date(string='Booking Date', default=fields.Date.context_today)
    ref = fields.Char(string='reference', help='reference of the patient from the patient record')
    patient_id = fields.Many2one(comodel_name='hospital.patient', string='patient')
    # Define HTML Field In Odoo
    prescription = fields.Html(string='Prescription')
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')
    # Add Statusbar In Odoo Development
    state = fields.Selection(
        [('draft', 'Draft'), ('in_consultation', 'In Consultation'), ('done', 'Done'), ('cancel', 'Cancelled')],
        default='draft', string="Status", required=True)

    # Define Onchange Functions
    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def action_test(self):
        print('click button')
        # Rainbow Effect 
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Click Successful',
                'type': 'rainbow_man',
            }
        }
