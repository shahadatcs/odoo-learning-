{
    'name': 'Hospital Management',
    'version': '1.0.0',
    'sequence': -100,
    'category': 'Hospital',
    'summary': 'Hospital management system',
    'description': """Hospital management system""",
    'depends': ['mail', 'product', 'base', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',

        'data/patient.tag.csv',
        'data/sequence_data.xml',
        'data/patient_tag_data.xml',
        'data/mail_template_data.xml',

        'report/report.xml',
        'report/patient_details_template.xml',
        'report/patient_card.xml',
        'report/appointment_details.xml',
        'report/all_patient_list.xml',

        'wizard/cancel_appointment_view.xml',
        'wizard/appointment_report_view.xml',
        'wizard/all_patient_report_view.xml',

        'views/res_config_settings_views.xml',
        'views/patient_tag_view.xml',
        'views/operation_view.xml',
        'views/patient_view.xml',
        'views/test.xml',
        'views/odoo_playground_view.xml',
        'views/appointment_view.xml',
        'views/kids_patient_view.xml',
        'views/male_patient_view.xml',
        'views/female_patient_view.xml',
        'views/menu.xml'

    ],
    'demo': [],
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'assets': {},
}
