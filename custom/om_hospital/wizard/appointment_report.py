from odoo import fields, models, api


class AppointmentReportWizard(models.TransientModel):
    _name = 'appointment.report.wizard'
    _description = 'Appointment Report Wizard'

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')

    def action_print_report(self):
        print("TU", self.read()[0], )
        domain = []
        patient_id = self.patient_id
        if patient_id:
            domain += [('patient_id', '=', patient_id.id)]
        date_from = self.date_from
        if date_from:
            domain += [('appointment_time', '>=', date_from)]
        date_to = self.date_to
        if date_to:
            domain += [('appointment_time', '<=', date_to)]
        # appointments = self.env['hospital.appointment'].search_read([])
        appointments = self.env['hospital.appointment'].search(domain)
        print('Appointments', appointments)
        appointment_list = []
        for appointment in appointments:
            vals = {
                'name': appointment.name,
                'gender': appointment.gender
            }
            appointment_list.append(vals)
        data = {
            'form_data': self.read()[0],
            'appointments': appointment_list
        }
        return self.env.ref('om_hospital.action_report_appointment_sh').report_action(self, data=data)

    def action_print_excel_report(self):
        appointments = self.env['hospital.appointment'].search_read([])
        print('Appointment', appointments)
        domain = []
        patient_id = self.patient_id
        if patient_id:
            domain += [('patient_id', '=', patient_id.id)]
        date_from = self.date_from
        if date_from:
            domain += [('appointment_time', '>=', date_from)]
        date_to = self.date_to
        if date_to:
            domain += [('appointment_time', '<=', date_to)]
        print('Domain.....................', domain)
        data = {
            'form_data': self.read()[0],
            'appointments': appointments
        }
        return self.env.ref('om_hospital.report_patient_appointment_xls').report_action(self, data=data)
