from odoo import api, fields, models
from datetime import date


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Cancel Appointment Wizard"

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    reason = fields.Text(string='Reason')

    def action_cancel(self):
        return
