import frappe

def get_context(context):
    plans = frappe.db.get_list('Insurance Plan',
        fields=['name','name1', 'description','company','annual_limit', 'number_of_dependants'],
    )
    insurance_companies = frappe.db.get_list('Insurance Company',
        fields=['name','name1','logo'],
    )

    context.plans = plans
    context.insurance_companies = insurance_companies
    return context
