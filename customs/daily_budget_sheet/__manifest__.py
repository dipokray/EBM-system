# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
	'name': 'Indent Management System',
	'version': '1.1',
	'sequence': 3,
	'category': 'Audit and Accounts',
	'depends': ['base', 'mail', 'hr_contract'],
	'description': """
Module for defining analytic accounting object.
===============================================

In Odoo, analytic accounts are linked to general accounts but are treated
totally independently. So, you can enter various different analytic operations
that have no counterpart in the general financial accounts.
    """,
	'data': [
		
		'view/indent_form.xml',
		'view/product.xml',
		'data/sequence.xml',
		# 'security/ir.model.access.csv',
		# 'security/security.xml',
		'report/Indent_form_report.xml',
	
	],
	
	'installable': True,
	'application': True,
	'auto_install': False,
}
