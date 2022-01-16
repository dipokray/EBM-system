# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Jewellery ',
    'version': '13.0.1.0.0',
    'category': 'Gold',
    'description': """

    """,
    'summary': ' ',
    # 'website': 'https://www.odoo.com/page/survey',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'views/order_view.xml',
        'views/product_create.xml',
        'views/sell_product.xml',
        'views/weight_config.xml',
        # 'wizard/button.xml',
        # 'security/ir.model.access.csv',
        'data/product_sequence.xml',
        'data/order_sequence.xml',

    ],
    'installable': True,
    'application': True,
}
