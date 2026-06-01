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
import datetime as DT
from odoo import http
from odoo.http import request


class HelpDeskDashboard(http.Controller):
    """Website helpdesk dashboard"""

    def _get_dashboard_values(self, date_domain=None, category_id=None):
        date_domain = date_domain or []
        category_domain = []
        if category_id:
            category_domain = [('category_id', '=', int(category_id))]
        stages = {
            'new': request.env['ticket.stage'].search(
                [('name', '=', 'Inbox')], limit=1).id,
            'draft': request.env['ticket.stage'].search(
                [('name', '=', 'Draft')], limit=1).id,
            'in_progress': request.env['ticket.stage'].search(
                [('name', '=', 'In Progress')], limit=1).id,
            'canceled': request.env['ticket.stage'].search(
                [('name', '=', 'Canceled')], limit=1).id,
            'done': request.env['ticket.stage'].search(
                [('name', '=', 'Done')], limit=1).id,
            'closed': request.env['ticket.stage'].search(
                [('name', '=', 'Closed')], limit=1).id,
        }
        dashboard_values = {}
        for key, stage_id in stages.items():
            domain = [('stage_id', '=', stage_id)] + date_domain + category_domain
            tickets = request.env["help.ticket"].search(domain)
            dashboard_values[key] = len(tickets)
            dashboard_values[f'{key}_id'] = tickets.ids
        return dashboard_values

    def _get_date_domain(self, period=None, start_date=None, end_date=None):
        today = DT.date.today()
        if period == 'this_week':
            return [('create_date', '>', (today - DT.timedelta(days=7)).isoformat())]
        if period == 'this_month':
            return [('create_date', '>', (today - DT.timedelta(days=30)).isoformat())]
        if period == 'this_year':
            return [('create_date', '>', (today - DT.timedelta(days=360)).isoformat())]
        if period == 'custom' and start_date and end_date:
            start = DT.date.fromisoformat(start_date)
            end = DT.date.fromisoformat(end_date)
            if start > end:
                start, end = end, start
            end_next_day = end + DT.timedelta(days=1)
            return [
                ('create_date', '>=', start.isoformat()),
                ('create_date', '<', end_next_day.isoformat()),
            ]
        return []

    @http.route(['/helpdesk_dashboard_categories'], type='json', auth="public")
    def helpdesk_dashboard_categories(self):
        """Return helpdesk categories for dashboard filters."""
        categories = request.env['helpdesk.categories'].search([])
        return [{'id': category.id, 'name': category.name} for category in categories]

    @http.route(['/helpdesk_dashboard_filtered'], type='json', auth="public")
    def helpdesk_dashboard_filtered(self, period=None, start_date=None,
                                    end_date=None, category_id=None):
        """Dashboard controller with period and category filters."""
        date_domain = self._get_date_domain(period, start_date, end_date)
        return self._get_dashboard_values(date_domain, category_id)

    @http.route(['/helpdesk_dashboard_custom'], type='json', auth="public")
    def helpdesk_dashboard_custom(self, start_date=None, end_date=None):
        """Date range based sorting controller"""
        date_domain = []
        if start_date and end_date:
            start = DT.date.fromisoformat(start_date)
            end = DT.date.fromisoformat(end_date)
            if start > end:
                start, end = end, start
            end_next_day = end + DT.timedelta(days=1)
            date_domain = [
                ('create_date', '>=', start.isoformat()),
                ('create_date', '<', end_next_day.isoformat()),
            ]
        return self._get_dashboard_values(date_domain)

    @http.route(['/helpdesk_dashboard'], type='json', auth="public")
    def helpdesk_dashboard(self):
        """Helpdesk dashboard controller"""
        stage_new = request.env['ticket.stage'].search(
            [('name', '=', 'Inbox')], limit=1).id
        stage_draft = request.env['ticket.stage'].search(
            [('name', '=', 'Draft')], limit=1).id
        stage_inprogress = request.env['ticket.stage'].search(
            [('name', '=', 'In Progress')], limit=1).id
        stage_canceled = request.env['ticket.stage'].search(
            [('name', '=', 'Canceled')], limit=1).id
        stage_done = request.env['ticket.stage'].search(
            [('name', '=', 'Done')], limit=1).id
        stage_closed = request.env['ticket.stage'].search(
            [('name', '=', 'Closed')], limit=1).id

        new = request.env["help.ticket"].search_count(
            [('stage_id', '=', stage_new)])
        new_id = request.env["help.ticket"].search(
            [('stage_id', '=', stage_new)])
        new_id_ls = [data.id for data in new_id]

        draft = request.env["help.ticket"].search_count(
            [('stage_id', '=', stage_draft)])
        draft_id = request.env["help.ticket"].search(
            [('stage_id', '=', stage_draft)])
        draft_id_ls = [data.id for data in draft_id]

        in_progress = request.env["help.ticket"].search_count(
            [('stage_id', '=', stage_inprogress)])
        in_progress_id = request.env["help.ticket"].search(
            [('stage_id', '=', stage_inprogress)])
        in_progress_ls = [data.id for data in in_progress_id]

        canceled = request.env["help.ticket"].search_count(
            [('stage_id', '=', stage_canceled)])
        canceled_id = request.env["help.ticket"].search(
            [('stage_id', '=', stage_canceled)])
        canceled_id_ls = [data.id for data in canceled_id]

        done = request.env["help.ticket"].search_count(
            [('stage_id', '=', stage_done)])
        done_id = request.env["help.ticket"].search(
            [('stage_id', '=', stage_done)])
        done_id_ls = [data.id for data in done_id]

        closed = request.env["help.ticket"].search_count(
            [('stage_id', '=', stage_closed)])
        closed_id = request.env["help.ticket"].search(
            [('stage_id', '=', stage_closed)])
        closed_id_ls = [data.id for data in closed_id]

        dashboard_values = {
            'new': new,
            'draft': draft,
            'in_progress': in_progress,
            'canceled': canceled,
            'done': done,
            'closed': closed,
            'new_id': new_id_ls,
            'draft_id': draft_id_ls,
            'in_progress_id': in_progress_ls,
            'canceled_id': canceled_id_ls,
            'done_id': done_id_ls,
            'closed_id': closed_id_ls,
        }
        return dashboard_values

    @http.route(['/helpdesk_dashboard_week'], type='json', auth="public")
    def helpdesk_dashboard_week(self):
        """Week based sorting controller"""
        today = DT.date.today()
        stage_new = request.env['ticket.stage'].search(
            [('name', '=', 'Inbox')], limit=1).id
        stage_draft = request.env['ticket.stage'].search(
            [('name', '=', 'Draft')], limit=1).id
        stage_inprogress = request.env['ticket.stage'].search(
            [('name', '=', 'In Progress')], limit=1).id
        stage_canceled = request.env['ticket.stage'].search(
            [('name', '=', 'Canceled')], limit=1).id
        stage_done = request.env['ticket.stage'].search(
            [('name', '=', 'Done')], limit=1).id
        stage_closed = request.env['ticket.stage'].search(
            [('name', '=', 'Closed')], limit=1).id

        week_ago = (today - DT.timedelta(days=7)).isoformat()

        new = request.env["help.ticket"].search_count(
            [('stage_id', '=', stage_new), ('create_date', '>', week_ago)])
        new_id = request.env["help.ticket"].search(
            [('stage_id', '=', stage_new), ('create_date', '>', week_ago)])
        new_id_ls = [data.id for data in new_id]

        draft = request.env["help.ticket"].search_count(
            [('stage_id', '=', stage_draft), ('create_date', '>', week_ago)])
        draft_id = request.env["help.ticket"].search(
            [('stage_id', '=', stage_draft), ('create_date', '>', week_ago)])
        draft_id_ls = [data.id for data in draft_id]

        in_progress = request.env["help.ticket"].search_count(
            [('stage_id', '=', stage_inprogress), ('create_date', '>', week_ago)])
        in_progress_id = request.env["help.ticket"].search(
            [('stage_id', '=', stage_inprogress), ('create_date', '>', week_ago)])
        in_progress_ls = [data.id for data in in_progress_id]

        canceled = request.env["help.ticket"].search_count(
            [('stage_id', '=', stage_canceled), ('create_date', '>', week_ago)])
        canceled_id = request.env["help.ticket"].search(
            [('stage_id', '=', stage_canceled), ('create_date', '>', week_ago)])
        canceled_id_ls = [data.id for data in canceled_id]

        done = request.env["help.ticket"].search_count(
            [('stage_id', '=', stage_done), ('create_date', '>', week_ago)])
        done_id = request.env["help.ticket"].search(
            [('stage_id', '=', stage_done), ('create_date', '>', week_ago)])
        done_id_ls = [data.id for data in done_id]

        closed = request.env["help.ticket"].search_count(
            [('stage_id', '=', stage_closed), ('create_date', '>', week_ago)])
        closed_id = request.env["help.ticket"].search(
            [('stage_id', '=', stage_closed), ('create_date', '>', week_ago)])
        closed_id_ls = [data.id for data in closed_id]

        dashboard_values = {
            'new': new,
            'draft': draft,
            'in_progress': in_progress,
            'canceled': canceled,
            'done': done,
            'closed': closed,
            'new_id': new_id_ls,
            'draft_id': draft_id_ls,
            'in_progress_id': in_progress_ls,
            'canceled_id': canceled_id_ls,
            'done_id': done_id_ls,
            'closed_id': closed_id_ls,
        }
        return dashboard_values

    @http.route(['/helpdesk_dashboard_month'], type='json', auth="public")
    def helpdesk_dashboard_month(self):
        """Month based sorting controller"""
        today = DT.date.today()
        stage_new = request.env['ticket.stage'].search(
            [('name', '=', 'Inbox')], limit=1).id
        stage_draft = request.env['ticket.stage'].search(
            [('name', '=', 'Draft')], limit=1).id
        stage_inprogress = request.env['ticket.stage'].search(
            [('name', '=', 'In Progress')], limit=1).id
        stage_canceled = request.env['ticket.stage'].search(
            [('name', '=', 'Canceled')], limit=1).id
        stage_done = request.env['ticket.stage'].search(
            [('name', '=', 'Done')], limit=1).id
        stage_closed = request.env['ticket.stage'].search(
            [('name', '=', 'Closed')], limit=1).id

        month_ago = (today - DT.timedelta(days=30)).isoformat()

        new = request.env["help.ticket"].search_count(
            [('stage_id', '=', stage_new), ('create_date', '>', month_ago)])
        new_id = request.env["help.ticket"].search(
            [('stage_id', '=', stage_new), ('create_date', '>', month_ago)])
        new_id_ls = [data.id for data in new_id]

        draft = request.env["help.ticket"].search_count(
            [('stage_id', '=', stage_draft), ('create_date', '>', month_ago)])
        draft_id = request.env["help.ticket"].search(
            [('stage_id', '=', stage_draft), ('create_date', '>', month_ago)])
        draft_id_ls = [data.id for data in draft_id]

        in_progress = request.env["help.ticket"].search_count(
            [('stage_id', '=', stage_inprogress), ('create_date', '>', month_ago)])
        in_progress_id = request.env["help.ticket"].search(
            [('stage_id', '=', stage_inprogress), ('create_date', '>', month_ago)])
        in_progress_ls = [data.id for data in in_progress_id]

        canceled = request.env["help.ticket"].search_count(
            [('stage_id', '=', stage_canceled), ('create_date', '>', month_ago)])
        canceled_id = request.env["help.ticket"].search(
            [('stage_id', '=', stage_canceled), ('create_date', '>', month_ago)])
        canceled_id_ls = [data.id for data in canceled_id]

        done = request.env["help.ticket"].search_count(
            [('stage_id', '=', stage_done), ('create_date', '>', month_ago)])
        done_id = request.env["help.ticket"].search(
            [('stage_id', '=', stage_done), ('create_date', '>', month_ago)])
        done_id_ls = [data.id for data in done_id]

        closed = request.env["help.ticket"].search_count(
            [('stage_id', '=', stage_closed), ('create_date', '>', month_ago)])
        closed_id = request.env["help.ticket"].search(
            [('stage_id', '=', stage_closed), ('create_date', '>', month_ago)])
        closed_id_ls = [data.id for data in closed_id]

        dashboard_values = {
            'new': new,
            'draft': draft,
            'in_progress': in_progress,
            'canceled': canceled,
            'done': done,
            'closed': closed,
            'new_id': new_id_ls,
            'draft_id': draft_id_ls,
            'in_progress_id': in_progress_ls,
            'canceled_id': canceled_id_ls,
            'done_id': done_id_ls,
            'closed_id': closed_id_ls,
        }
        return dashboard_values

    @http.route(['/helpdesk_dashboard_year'], type='json', auth="public")
    def helpdesk_dashboard_year(self):
        """Year based sorting"""
        today = DT.date.today()
        stage_new = request.env['ticket.stage'].search(
            [('name', '=', 'Inbox')], limit=1).id
        stage_draft = request.env['ticket.stage'].search(
            [('name', '=', 'Draft')], limit=1).id
        stage_inprogress = request.env['ticket.stage'].search(
            [('name', '=', 'In Progress')], limit=1).id
        stage_canceled = request.env['ticket.stage'].search(
            [('name', '=', 'Canceled')], limit=1).id
        stage_done = request.env['ticket.stage'].search(
            [('name', '=', 'Done')], limit=1).id
        stage_closed = request.env['ticket.stage'].search(
            [('name', '=', 'Closed')], limit=1).id

        year_ago = (today - DT.timedelta(days=360)).isoformat()

        new = request.env["help.ticket"].search_count(
            [('stage_id', '=', stage_new), ('create_date', '>', year_ago)])
        new_id = request.env["help.ticket"].search(
            [('stage_id', '=', stage_new), ('create_date', '>', year_ago)])
        new_id_ls = [data.id for data in new_id]

        draft = request.env["help.ticket"].search_count(
            [('stage_id', '=', stage_draft), ('create_date', '>', year_ago)])
        draft_id = request.env["help.ticket"].search(
            [('stage_id', '=', stage_draft), ('create_date', '>', year_ago)])
        draft_id_ls = [data.id for data in draft_id]

        in_progress = request.env["help.ticket"].search_count(
            [('stage_id', '=', stage_inprogress), ('create_date', '>', year_ago)])
        in_progress_id = request.env["help.ticket"].search(
            [('stage_id', '=', stage_inprogress), ('create_date', '>', year_ago)])
        in_progress_ls = [data.id for data in in_progress_id]

        canceled = request.env["help.ticket"].search_count(
            [('stage_id', '=', stage_canceled), ('create_date', '>', year_ago)])
        canceled_id = request.env["help.ticket"].search(
            [('stage_id', '=', stage_canceled), ('create_date', '>', year_ago)])
        canceled_id_ls = [data.id for data in canceled_id]

        done = request.env["help.ticket"].search_count(
            [('stage_id', '=', stage_done), ('create_date', '>', year_ago)])
        done_id = request.env["help.ticket"].search(
            [('stage_id', '=', stage_done), ('create_date', '>', year_ago)])
        done_id_ls = [data.id for data in done_id]

        closed = request.env["help.ticket"].search_count(
            [('stage_id', '=', stage_closed), ('create_date', '>', year_ago)])
        closed_id = request.env["help.ticket"].search(
            [('stage_id', '=', stage_closed), ('create_date', '>', year_ago)])
        closed_id_ls = [data.id for data in closed_id]

        dashboard_values = {
            'new': new,
            'draft': draft,
            'in_progress': in_progress,
            'canceled': canceled,
            'done': done,
            'closed': closed,
            'new_id': new_id_ls,
            'draft_id': draft_id_ls,
            'in_progress_id': in_progress_ls,
            'canceled_id': canceled_id_ls,
            'done_id': done_id_ls,
            'closed_id': closed_id_ls,
        }
        return dashboard_values
