# -*- coding: utf-8 -*-

from odoo import api, models


class IrActionsActWindow(models.Model):
    _inherit = 'ir.actions.act_window'

    @api.model
    def _register_hook(self):
        res = super()._register_hook()
        actions = self.env['ir.actions.act_window'].sudo().search([
            ('res_model', 'in', [
                'help.ticket',
                'help.team',
                'ticket.stage',
                'helpdesk.categories',
                'helpdesk.tag',
                'helpdesk.types',
            ])
        ])
        for action in actions:
            vals = {}
            if action.view_mode and 'tree' in action.view_mode:
                vals['view_mode'] = action.view_mode.replace('tree', 'list')
            view_values = [
                (view_id, 'list' if view_type == 'tree' else view_type)
                for view_id, view_type in action.views
            ]
            if view_values != list(action.views):
                vals['views'] = view_values
            if vals:
                action.write(vals)
        return res
