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
        [('draft', 'Draft'), ('in_consultation', 'In Consultation'), ('done', 'Done'), ('cancel', 'Cancelled'),
         ('warning', 'Warning')],
        default='draft', string="Status", required=True)
    doctor_id = fields.Many2one('res.users', string='Doctor')
    pharmacy_lines_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string='Pharmacy')
    hide_sales_price = fields.Boolean(string='Hide sales price')

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

    def action_in_consultation(self):
        for rec in self:
            rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    # def action_cancel(self):
    #     for rec in self:
    #         rec.state = 'cancel'

    def action_cancel(self):
        self.state = 'cancel'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_warning(self):
        for rec in self:
            rec.state = 'warning'

    class AppointmentPharmacyLines(models.Model):
        _name = "appointment.pharmacy.lines"
        _description = "Appointment Pharmacy Lines"

        product_id = fields.Many2one('product.product', required=True)
        price_unit = fields.Float(related='product_id.list_price')
        qty = fields.Integer(string='Quantity', default=1)
        appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
