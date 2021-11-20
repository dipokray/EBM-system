# -*- coding: utf-8 -*-
{
    'name': 'Employee Expense Management',
    'version': '1.0',
    'summary': 'Employee Expense Management Software',
    'sequence': -100,
    'description': """ Employee Expense Management Software """,
    'category': 'Productivity',
    'website': 'https://yukoleather.net/',
    'license': 'LGPL-3',
    'depends': ['mail',
                'hr',
                'base',
                'IOU_Management',
                ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'wizard/create_iou_view.xml',
        'views/menu_view.xml',
        'views/ebm_view.xml',
        'views/product_view.xml',
        'report/ebm_details_report.xml',
        'report/pre_costing_details_report.xml',
        'report/bill_report.xml',
        'report/bill_summary_report.xml',
        'report/report.xml',


    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
