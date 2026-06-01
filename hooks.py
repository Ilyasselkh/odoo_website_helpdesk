# -*- coding: utf-8 -*-

def _fix_legacy_tree_view_modes(env):
    action_xmlids = [
        'odoo_website_helpdesk.help_ticket_action',
        'odoo_website_helpdesk.help_ticket_my_ticket_action',
        'odoo_website_helpdesk.help_ticket_report_action',
        'odoo_website_helpdesk.help_team_action',
        'odoo_website_helpdesk.ticket_stage_action',
        'odoo_website_helpdesk.helpdesk_categories_action',
        'odoo_website_helpdesk.helpdesk_tag_action',
        'odoo_website_helpdesk.helpdesk_types_action',
    ]
    for xmlid in action_xmlids:
        action = env.ref(xmlid, raise_if_not_found=False)
        if not action or action._name != 'ir.actions.act_window':
            continue
        vals = {}
        if action.view_mode and 'tree' in action.view_mode:
            vals['view_mode'] = action.view_mode.replace('tree', 'list')
        view_values = []
        for view_id, view_type in action.views:
            view_values.append((view_id, 'list' if view_type == 'tree' else view_type))
        if view_values != list(action.views):
            vals['views'] = view_values
        if vals:
            action.write(vals)


def post_init_hook(env):
    _fix_legacy_tree_view_modes(env)
