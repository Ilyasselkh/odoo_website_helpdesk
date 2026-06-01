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
import html

from odoo import http
from odoo.addons.portal.controllers import portal
from odoo.http import request


class TicketPortal(portal.CustomerPortal):
    """ Controller for handling customer portal related actions related to
    helpdesk tickets.
    """
    def _prepare_home_portal_values(self, counters):
        """Prepares a dictionary of values to be used in the home portal view
        and get their count."""
        values = super()._prepare_home_portal_values(counters)
        if 'ticket_count' in counters:
            ticket_count = request.env['help.ticket'].search_count(
                self._get_tickets_domain()) if request.env[
                'help.ticket'].check_access_rights(
                'read', raise_exception=False) else 0
            values['ticket_count'] = ticket_count
        return values

    def _get_tickets_domain(self):
        """Checking the domain"""
        return [('customer_id', '=', request.env.user.partner_id.id)]

    @http.route(['/my/tickets'], type='http', auth="user", website=True)
    def portal_my_tickets(self):
        """Displays a list of tickets for the current user in the user's
        portal."""
        domain = self._get_tickets_domain()
        tickets = request.env['help.ticket'].search(domain)
        values = {
            'default_url': "/my/tickets",
            'tickets': tickets,
            'page_name': 'ticket',
        }
        return request.render("odoo_website_helpdesk.portal_my_tickets",
                              values)

    @http.route(['/my/tickets/<int:id>'], type='http', auth="public",
                website=True)
    def portal_tickets_details(self, id):
        """Displays a list of tickets for the current user in the user's
        portal."""
        details = request.env['help.ticket'].sudo().search([('id', '=', id)])
        data = {
            'page_name': 'ticket',
            'ticket': True,
            'details': details,
        }
        return request.render("odoo_website_helpdesk.portal_ticket_details",
                              data)

    @http.route('/my/tickets/download/<id>', auth='public',
                type='http',
                website=True)
    def ticket_download_portal(self, id):
        """Download the ticket information in a pdf formate of the current
         event ticket."""
        data = {
            'help': request.env['help.ticket'].sudo().browse(int(id))}
        report = request.env.ref(
            'odoo_website_helpdesk.action_report_helpdesk_ticket')
        pdf, _ = request.env.ref(
            'odoo_website_helpdesk.action_report_helpdesk_ticket').sudo()._render_qweb_pdf(
            report, data=data)
        pdf_http_headers = [('Content-Type', 'application/pdf'),
                            ('Content-Length', len(pdf)),
                            ('Content-Disposition',
                             'attachment; filename="Helpdesk Ticket.pdf"')]
        return request.make_response(pdf, headers=pdf_http_headers)


class WebsiteDesk(http.Controller):
    """Control for handling the helpdesk tickets form and its submission."""
    @http.route(['/helpdesk_ticket'], type='http', auth="public",
                website=True, sitemap=True)
    def helpdesk_ticket(self):
        """Render the helpdesk ticket form."""
        types = request.env['helpdesk.types'].sudo().search([])
        categories = request.env['helpdesk.categories'].sudo().search([])
        type_options = ''.join(
            f'<option value="{ticket_type.id}">{html.escape(ticket_type.name or "")}</option>'
            for ticket_type in types
        )
        category_options = ''.join(
            f'<option value="{category.id}">{html.escape(category.name or "")}</option>'
            for category in categories
        )
        csrf_token = html.escape(request.csrf_token())
        html_content = f"""
            <!doctype html>
            <html>
                <head>
                    <title>Support Tickets</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1"/>
                    <style>
                        body {{
                            margin: 0;
                            font-family: Arial, sans-serif;
                            color: #111827;
                            background: #fff;
                        }}
                        header {{
                            height: 60px;
                            display: flex;
                            align-items: center;
                            gap: 32px;
                            padding: 0 16%;
                            border-bottom: 1px solid #e5e7eb;
                        }}
                        header a {{
                            color: #1f2937;
                            text-decoration: none;
                            font-size: 16px;
                        }}
                        .brand {{
                            font-size: 34px;
                            letter-spacing: -1px;
                        }}
                        .hero {{
                            min-height: 185px;
                            padding: 32px 16%;
                            color: #fff;
                            background: linear-gradient(rgba(0,0,0,.45), rgba(0,0,0,.45)),
                                url('/web/image/website.s_banner_default_image') center / cover;
                        }}
                        .hero h1 {{
                            margin: 0 0 12px;
                            font-size: 48px;
                            font-weight: 700;
                        }}
                        .hero a {{
                            display: inline-block;
                            padding: 16px 42px;
                            border-radius: 32px;
                            color: #111827;
                            background: #f3f4f6;
                            text-decoration: none;
                            font-size: 22px;
                        }}
                        main {{
                            max-width: 920px;
                            margin: 42px auto;
                            padding: 0 24px 60px;
                        }}
                        .intro {{
                            font-size: 22px;
                            line-height: 1.45;
                            margin-bottom: 34px;
                        }}
                        .field {{
                            display: grid;
                            grid-template-columns: 180px minmax(0, 1fr);
                            gap: 20px;
                            align-items: start;
                            margin: 24px 0;
                        }}
                        label {{
                            padding-top: 8px;
                            font-size: 17px;
                        }}
                        input, select, textarea {{
                            width: 100%;
                            box-sizing: border-box;
                            border: 1px solid #d1d5db;
                            border-radius: 6px;
                            padding: 10px 12px;
                            font-size: 17px;
                            background: #fff;
                        }}
                        textarea {{
                            min-height: 64px;
                            resize: vertical;
                        }}
                        button {{
                            margin-left: 200px;
                            border: 0;
                            border-radius: 32px;
                            padding: 18px 42px;
                            color: #fff;
                            background: #2f6091;
                            font-size: 21px;
                            font-weight: 700;
                            cursor: pointer;
                        }}
                        footer {{
                            padding: 22px 16%;
                            color: #fff;
                            background: #343a40;
                        }}
                        @media (max-width: 720px) {{
                            header, .hero {{
                                padding-left: 24px;
                                padding-right: 24px;
                            }}
                            .field {{
                                grid-template-columns: 1fr;
                                gap: 8px;
                            }}
                            button {{
                                margin-left: 0;
                                width: 100%;
                            }}
                        }}
                    </style>
                </head>
                <body>
                    <header>
                        <div class="brand">ARaymond</div>
                        <a href="/">Home</a>
                        <a href="/processus">Processus</a>
                    </header>
                    <section class="hero">
                        <h1>Support Tickets</h1>
                        <a href="/my/tickets">Consulter mes tickets</a>
                    </section>
                    <main>
                        <div class="intro">
                            Open a ticket for any issue or request related to SAP here.<br/>
                            We'll do our best to get back to you as soon as possible.
                        </div>
                        <form id="Ticket_form" action="/helpdesk_ticket/submit" method="post" enctype="multipart/form-data">
                            <input type="hidden" name="csrf_token" value="{csrf_token}"/>
                            <div class="field">
                                <label for="ticket_type">Ticket type *</label>
                                <select id="ticket_type" name="ticket_type" required>{type_options}</select>
                            </div>
                            <div class="field">
                                <label for="category">Category *</label>
                                <select id="category" name="category" required>{category_options}</select>
                            </div>
                            <div class="field">
                                <label for="subject">Subject *</label>
                                <input id="subject" name="subject" required/>
                            </div>
                            <div class="field">
                                <label for="description">Description</label>
                                <textarea id="description" name="description" required></textarea>
                            </div>
                            <div class="field">
                                <label for="ticket_attachment">Attachment</label>
                                <input id="ticket_attachment" type="file" name="ticket_attachment" multiple/>
                            </div>
                            <button type="submit">Submit</button>
                        </form>
                    </main>
                    <footer>Araymond MAROC</footer>
                </body>
            </html>
        """
        return request.make_response(html_content)

    @http.route(['/rating/<int:ticket_id>'], type='http', auth="public",
                website=True,
                sitemap=True)
    def rating(self, ticket_id):
        """Render the helpdesk ticket rating form."""
        ticket = request.env['help.ticket'].browse(ticket_id)
        data = {
            'ticket': ticket.id,
        }
        return request.render('odoo_website_helpdesk.rating_form', data)

    @http.route(['/rating/<int:ticket_id>/submit'], type='http',
                auth="user",
                website=True, csrf=False,
                sitemap=True)
    def rating_backend(self, ticket_id, **post):
        """Render the thanks page after rating the helpdesk ticket."""
        ticket = request.env['help.ticket'].browse(ticket_id)
        ticket.write({
            'customer_rating': post['rating'],
            'review': post['message'],
        })
        return request.render('odoo_website_helpdesk.rating_thanks')
