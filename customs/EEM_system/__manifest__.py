# -*- coding: utf-8 -*-
{
    'name': 'EEM System',
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
                ],
    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        # 'wizard/create_iou_view.xml',
        'views/eem_product_view.xml',
        'views/eem_pre_costing_view.xml',
        'views/eem_bill_view.xml',
        # 'report/ebm_details_report.xml',
        # 'report/pre_costing_details_report.xml',
        # 'report/bill_report.xml',
        # 'report/bill_summary_report.xml',
        # 'report/report.xml',


    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
