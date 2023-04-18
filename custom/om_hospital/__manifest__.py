{
    'name': 'Hospital Management',
    'version': '1.0.0',
    'sequence': -100,
    'category': 'Hospital',
    'summary': 'Hospital management system',
    'description': """Hospital management system""",
    'depends': ['mail', 'product', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'data/patient.tag.csv',
        'data/sequence_data.xml',
        'data/patient_tag_data.xml',

        'views/patient_tag_view.xml',
        'wizard/cancel_appointment_view.xml',
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
