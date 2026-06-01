# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import api, fields, models


class HelpTeam(models.Model):
    """ This class represents a Helpdesk Team in the system, providing
     information about the team members, leader, and related project."""
    _name = 'help.team'
    _description = 'Helpdesk Team'

    name = fields.Char(string='Name', help='Name of the Helpdesk Team. It '
                                           'identify the helpdesk team')
    team_lead_id = fields.Many2one(
        'res.users',
        string='Team Leader',
        help='Name of the Helpdesk Team Leader.',
        domain=lambda self: self._users_in_group_domain(
            'odoo_website_helpdesk.helpdesk_team_leader'))
    member_ids = fields.Many2many(
        'res.users',
        string='Members',
        help='Users who belong to that Helpdesk Team',
        domain=lambda self: self._users_in_group_domain(
            'odoo_website_helpdesk.helpdesk_user'))
    email = fields.Char(string='Email', help='Email')
    project_id = fields.Many2one('project.project',
                                 string='Project',
                                 help='The Project they are currently in')
    create_task = fields.Boolean(string="Create Task",
                                 help="Enable for allowing team to "
                                      "create tasks from tickets")

    def _users_in_group_domain(self, xmlid):
        users = self.env['res.users'].sudo().search([]).filtered(
            lambda user: user.has_group(xmlid))
        return [('id', 'in', users.ids)]

    @api.onchange('team_lead_id')
    def members_choose(self):
        """ This method is triggered when the Team Leader is changed. It
        updates the available team members based on the selected leader and
        filters out the leader from the list of potential members."""
        filtered_members = self.env['res.users'].sudo().search([]).filtered(
            lambda user: user.has_group('odoo_website_helpdesk.helpdesk_user')
            and not user.has_group('odoo_website_helpdesk.helpdesk_team_leader'))
        filtered_members = filtered_members.filtered(
            lambda user: user.id != self.team_lead_id.id)
        return {'domain': {'member_ids': [
            ('id', 'in', filtered_members.ids)]}}
