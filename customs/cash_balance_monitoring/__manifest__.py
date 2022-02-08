# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Yuko Cash Monitoring',
    'version': '13.0.1.0.0',
    'category': 'Tk',
    'description': """

    """,
    'summary': ' ',
    'website': 'https://www.odoo.com/page/survey',
    'depends': [
        'web',
        'board',
        'contacts',
        'mail'
    ],
    'data': [
        'views/cashin.xml',
        # 'views/cashout.xml',
    ],
    'installable': True,
    'application': True,
}
