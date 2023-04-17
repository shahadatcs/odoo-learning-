from odoo import api, fields, models
from datetime import date
import datetime


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Cancel Appointment Wizard"

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res['cancel_date'] = datetime.date.today()
        return res

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    reason = fields.Text(string='Reason', default='test reason')
    cancel_date = fields.Date(string='Cancellation Date')

    def action_cancel(self):
        return

