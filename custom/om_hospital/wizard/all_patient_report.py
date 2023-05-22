from odoo import fields, models, api


class PatientReportWizard(models.TransientModel):
    _name = 'patient.report.wizard'
    _description = 'Patient Report Wizard'

    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('kids', 'Kids'), ('neuter', 'Neuter'), ('common', 'Common'),
         ('other', 'Other')], string='Gender')
    age = fields.Integer(string='Age')

    def action_print_reports(self):
        data = {
            'form_data': self.read()[0]
        }
        return self.env.ref('om_hospital.action_patient').report_action(self, data=data)
