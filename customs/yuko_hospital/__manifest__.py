# -*- coding: utf-8 -*-
{
    'name': 'Hospital Management',
    'version': '1.0',
    'summary': 'Hospital Management Software',
    'sequence': -100,
    'description': """ Hospital Management Software """,
    'category': 'Productivity',
    'website': 'https://yukoleather.net/',
    'license': 'LGPL-3',
    'depends': ['sale',
                'mail'],
    'data': [
        # 'security/ir.model.access.csv',
        'data/data.xml',
        'wizard/create_appointment_view.xml',
        'wizard/search_appointment_view.xml',
        'wizard/appointment_report_view.xml',
        'views/patient_view.xml',
        'views/kids_view.xml',
        'views/patient_gender_view.xml',
        'views/appointment_view.xml',
        'views/doctor_view.xml',
        'views/menu.xml',
        'views/sale.xml',
        'report/patient_card.xml',
        # 'report/patient_details_template.xml',
        'report/appointment_details.xml',
        'report/report.xml'

    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
