# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Yuko Visitor management System',
    'version': '13.0.1.0.0',
    'category': 'Visitor',
    'description': """

    """,
    'summary': ' ',
    'website': 'https://www.odoo.com/page/survey',
    'depends': [
        'base',
        'hr',
        'contacts',
        'mail',
        'sale',
        # 'web_widget_image_webcam',
        # 'whatsapp_redirect',


    ],
    'data': [
        'views/visitor.xml',
        'views/visit.xml',
        # 'views/test.xml',
        # 'views/re_visit.xml',
        'security/ir.model.access.csv',
        'security/security_group.xml',
        'data/sequence.xml',
        'data/mail_template.xml',

    ],
    'installable': True,
    'application': True,
}
