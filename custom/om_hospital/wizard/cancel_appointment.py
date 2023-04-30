from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import date
from dateutil import relativedelta
import datetime


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Cancel Appointment Wizard"

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res['cancel_date'] = datetime.date.today()
        if self.env.context.get('active_id'):
            res['appointment_id'] = self.env.context.get('active_id')
        return res

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment',
                                     domain=['|', ('state', '=', 'draft'), ('priority', 'in', (0, 1))])
    reason = fields.Text(string='Reason', default='test reason')
    cancel_date = fields.Date(string='Cancellation Date')

    def action_cancel(self):
        # action = self.env.ref('om_hospital.action_hospital_appointment').read()[0]
        cancel_days = self.env['ir.config_parameter'].get_param('om_hospital.cancel_days')
        allowed_day = date.today() - relativedelta.relativedelta(days=int(cancel_days))
        print('Cancel Days', allowed_day)
        if allowed_day > date.today():
            raise ValidationError('Sorry, Cancellation is not allowed for booking')
        # #action['domain'] = [('patient_id', '=', self.patient_id.id)]
        # return action
