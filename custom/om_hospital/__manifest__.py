{
    'name': 'Hospital Management',
    'version': '1.0.0',
    'sequence': -100,
    'category': 'Hospital',
    'summary': 'Hospital management system',
    'description': """Hospital management system""",
    'depends': ['mail'],
    'data': [
        'security/ir.model.access.csv',

        'views/patient_view.xml',
        'views/appointment_view.xml',
        'views/kids_patient_view.xml',
        'views/male_patient_view.xml',
        'views/female_patient_view.xml',
        'views/menu.xml',
    ],
    'demo': [],
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'assets': {},
}
