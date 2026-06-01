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
from ast import literal_eval

from odoo import fields, models


class MailComposeMessage(models.TransientModel):
    """ This class extends the functionality of the 'mail.compose.message'
    model to include custom behavior for sending emails related to help tickets.
   """
    _inherit = 'mail.compose.message'

    def _action_send_mail(self, auto_commit=False):
        """Override of the base '_action_send_mail' method to include additional
        logic when sending emails related to help tickets.

        If the model associated with the mail is 'help.ticket', update the
        'replied_date' field of the associated help ticket to the current date.
        """
        for wizard in self:
            if wizard.model != 'help.ticket':
                continue
            res_ids = wizard._get_help_ticket_res_ids()
            if res_ids:
                self.env['help.ticket'].browse(res_ids).write({
                    'replied_date': fields.Date.today(),
                })
        return super()._action_send_mail(auto_commit=auto_commit)

    def _get_help_ticket_res_ids(self):
        """Return target ticket ids for Odoo versions using res_id or res_ids."""
        self.ensure_one()
        if 'res_ids' in self._fields:
            res_ids = self.res_ids
            if isinstance(res_ids, str):
                try:
                    res_ids = literal_eval(res_ids or '[]')
                except (ValueError, SyntaxError):
                    res_ids = []
            if isinstance(res_ids, int):
                return [res_ids]
            return [res_id for res_id in (res_ids or []) if res_id]
        if 'res_id' in self._fields and self.res_id:
            return [self.res_id]
        return []
