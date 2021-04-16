import json
import requests
import frappe

def get_context(context):
    #plan
    args = frappe.request.args
    user = frappe.session.user
    plan = frappe.db.get_list('Insurance Plan',
        filters={
            'name': args['plan_name']
        },
        fields=['name','name1', 'description','company','annual_limit', 'number_of_dependants'],
    )
    print(plan)
    #supporter
    supporter =  frappe.db.get_list('Supporter',
        filters={
            'user' : user
        },
        fields = ['name','user','first_name','middle_name','last_name','email','phone_number','gender','country']
    )

    merchantCode = '0628420098'
    username = '0628420098'
    password = '5GW2dJT4KIaNlX4RRPJa56c4eSn6ZBLpq'
    api_key = 'Basic QW5KaDdMTmIzaERvd0E2d1R3UkQ1MXAxWUVJdk9qcnU6NjZkb09HMXdYMlRMZDA0aQ=='

    merchant_name = 'Designdock KE'
    url = "https://api-test.equitybankgroup.com/v1/token"

    payload = {
        "grant_type": 'password',
        "merchantCode":username,
        "password":password
    }
    headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization":api_key
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response)
    print(response.text)
    test = json.loads(response.text)
    context.plan = plan[0]
    context.supporter = supporter
    context.payment_token = test['payment-token']
    context.merchant_code = merchantCode
    context.merchant_name = merchant_name
    context.outlet_code = "0000000000"
    return context
