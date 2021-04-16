import frappe

def get_context(context):
    args = frappe.request.args
    plan = frappe.db.get_list('Insurance Plan',
        filters={
            'name': args['plan_name']
        },
        fields=['name','name1', 'description','company','annual_limit', 'number_of_dependants'],
    )

    # plan limits
    plan_limits = frappe.db.get_list('Plan Limit',
        filters={
            'plan': args['plan_name']
        },
        fields=['limit_name','limit_amount'],
    )
    #plan covers
    plan_covers = frappe.db.get_list('Plan Cover',
        filters={
            'plan': args['plan_name']
        },
        fields=['cover','covered'],
    )
    # complex stuff coz i couldnt find foreign key lookup filter...arrggh frappe
    covered = []
    not_covered = []
    for plan_cover in plan_covers:
        cover = frappe.db.get_list('Cover',
            filters={
                'name': plan_cover.cover
            },
            fields=['description'],
        )
        if plan_cover.covered == 1:
            covered.append(cover[0])
        else:
            not_covered.append(cover[0])

    # all plans
    plans = frappe.db.get_list('Insurance Plan',
        fields=['name','name1', 'description','company','annual_limit', 'number_of_dependants'],
    )

    plans_dict = []
    # details for al the plans
    for plan in plans:
        # plan limits
        plan_limits = frappe.db.get_list('Plan Limit',
            filters={
                'plan': plan.name
            },
            fields=['limit_name','limit_amount'],
        )
        #plan covers
        plan_covers = frappe.db.get_list('Plan Cover',
            filters={
                'plan': plan.name
            },
            fields=['cover','covered'],
        )
        # complex stuff coz i couldnt find foreign key lookup filter...arrggh frappe
        covered = []
        not_covered = []
        for plan_cover in plan_covers:
            cover = frappe.db.get_list('Cover',
                filters={
                    'name': plan_cover.cover
                },
                fields=['description'],
            )
            if plan_cover.covered == 1:
                covered.append(cover[0])
            else:
                not_covered.append(cover[0])
        plans_dict.append(
            {
                "detail":plan,
                "plan_limits":plan_limits,
                "covered":covered,
                "not_covered":not_covered
            }
        )
        print(plans_dict)

    context.plan = plan
    context.plan_limits = plan_limits
    context.covered = covered
    context.not_covered = not_covered
    context.plans = plans_dict
    return context
