from __future__ import unicode_literals
import frappe

def get_context(context):
    args = frappe.request.args
    user = frappe.session.user

    #plan
    plan = frappe.db.get_list('Insurance Plan',
        filters={
            'name': args['plan_name']
        },
        fields=['name','name1', 'description','company','annual_limit', 'number_of_dependants'],
    )
    #supporter
    supporter =  frappe.db.get_list('Supporter',
        filters={
            'user' : user
        },
        fields = ['name','user','first_name','middle_name','last_name','email','phone_number','gender','country']
    )
    #beneficiaries
    beneficiaries = []
    print(supporter)
    new_supporter = False
    if len(supporter) > 0: #
        supporter = supporter[0]
        beneficiaries = frappe.db.get_list('Beneficiary',
            filters={
                'supporter': supporter.name
            },
            fields = ['relation_to_supporter','name','first_name','middle_name','last_name','email','phone_number','gender','country']

        )
    else:
        new_supporter = True
        supporter = frappe.db.get_value("User", user, ['full_name','email','first_name','middle_name','last_name'],as_dict=True)
        print(supporter)


    #relations
    relations = frappe.db.get_list('Supporter Beneficiary Relation',
        fields = ['name1','name']
    )
    #countries
    countries = frappe.db.get_list('OriginCountry',
        fields = ['name1','name']
    )

    context.plan = plan[0]
    context.supporter = supporter
    context.beneficiaries = beneficiaries
    context.relations = relations
    context.countries = countries
    context.new_supporter = new_supporter
    return context



@frappe.whitelist(allow_guest = True)
def add_supporter(new_supporter,supporter_id,first_name,last_name,middle_name,email,phone_number,date_of_birth,gender,country):
    user = frappe.session.user
    new_supporter = eval(new_supporter)
    supporter = None
    if new_supporter:
        # new supporter
        supporter = frappe.new_doc('Supporter')
        supporter.update({
            'user': user,
            'first_name': first_name,
            'last_name': last_name,
            'middle_name': middle_name,
            'email': email,
            'phone_number': phone_number,
            'date_of_birth': date_of_birth,
            'gender': gender,
            'country': country
        })
        supporter.insert()
    else:
        # not new supporter here
        supporter = frappe.get_doc('Supporter', supporter_id)
        supporter.update({
            'user': user,
            'first_name': first_name,
            'last_name': last_name,
            'middle_name': middle_name,
            'email': email,
            'phone_number': phone_number,
            'date_of_birth': date_of_birth,
            'gender': gender,
            'country': country
        })
        supporter.save()
    return supporter


@frappe.whitelist(allow_guest = True)
def add_beneficiary(supporter_id,first_name,last_name,middle_name,email,phone_number,date_of_birth,gender,country,relation):
    # new beneficiary
    beneficiary = frappe.new_doc('Beneficiary')
    beneficiary.update({
        'supporter': supporter_id,
        'first_name': first_name,
        'last_name': last_name,
        'middle_name': middle_name,
        'email': email,
        'phone_number': phone_number,
        'date_of_birth': date_of_birth,
        'gender': gender,
        'country': country,
        'relation_to_supporter':relation
    })
    beneficiary.insert()
    return beneficiary
