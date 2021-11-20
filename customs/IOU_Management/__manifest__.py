# -*- coding: utf-8 -*-
{
    'name': 'IOU Management',
    'version': '1.0',
    'summary': 'IOU Management Software',
    'sequence': -100,
    'description': """ IOU Management Software """,
    'category': 'Productivity',
    'website': 'https://yukoleather.net/',
    'license': 'LGPL-3',
    'depends': ['mail',
                'hr',
                'base',
                ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'views/menu_view.xml',
        'views/iou_view.xml',


    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
