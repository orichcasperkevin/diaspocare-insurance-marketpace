from __future__ import unicode_literals

import frappe

def get_context(context):
	print(frappe.form_dict)
	context.test = "nfkne"
	return context
