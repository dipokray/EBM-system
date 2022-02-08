# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Gate Pass Management',
    'version': '13.0.1.0.0',
    'category': 'gate_pass',
    'description': """

    """,
    'summary': ' ',
    'website': 'https://www.odoo.com/page/survey',
    'depends': [
        'base',
        'hr',
        'contacts',
        'mail',

    ],
    'data': [
        'views/gate.xml',
        # 'security/ir.model.access.csv',
        # 'security/security.xml',

    ],
    'installable': True,
    'application': True,
}
