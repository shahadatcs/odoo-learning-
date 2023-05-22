from odoo import models, api, fields


class AllPatientReport(models.AbstractModel):
    _name = 'report.om_hospital.report_patient_id_details'
    _description = 'Patient Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        print('Testing..............', docids, data)
        domain = []
        gender = data.get('form_data').get('gender')
        age = data.get('form_data').get('age')
        if gender:
            domain += [('gender', '=', gender)]
        if age != 0:
            domain += [('age', '=', age)]
        docs = self.env['hospital.patient'].search(domain)
        return {
            'docs': docs,
            'email': 'sh@gmail.com'
        }


class PatientDetailsReport(models.AbstractModel):
    _name = 'report.om_hospital.report_patient_detail'
    _description = 'Patient Details Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        print('testing......', docids, data)
        docs = self.env['hospital.patient'].browse(docids)
        docs = self.env['hospital.patient'].search([('id', '=', docids)])
        return {
            'docs': docs
        }
