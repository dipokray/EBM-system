# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Indent System',
    'version': '13.0.1.0.0',
    'category': 'commercial',
    'description': """

    """,
    'summary': ' ',
    'website': 'https://www.odoo.com/page/survey',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'views/import_view.xml',
        'views/export_view.xml',
        'views/dynamic_bank_exp_import.xml',
        'views/dynamic_documents.xml',
        'views/dynamic_cnf.xml',
        'views/dynamic_courier.xml',
        'views/dynamic_forwarder.xml',
        'views/dynamic_insurance.xml',
        'views/dynamic_transportation.xml',
        'views/exp_dynamic_bank.xml',
        'views/exp_dynamic_cnf.xml',
        'views/exp_dynamic_courier.xml',
        'views/exp_dynamic_doc.xml',
        'views/exp_dynamic_forwarder.xml',
        'views/exp_transportation.xml',
        'data/sequence.xml',
        'data/export_sequence.xml',
        'report/import_report.xml',
        'security/ir.model.access.csv',


    ],
    'installable': True,
    'application': True,
}
