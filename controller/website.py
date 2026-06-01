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
import base64
import html
import json
from odoo import _, http
from psycopg2 import IntegrityError
from odoo.http import request
from odoo.exceptions import ValidationError
from odoo.addons.website.controllers.form import WebsiteForm


class HelpdeskProduct(http.Controller):
    """It controls the website products and return the product."""
    @http.route('/product', auth='public', type='json')
    def product(self):
        """Product control function"""
        products = request.env['product.template'].sudo().search_read([],
                                                                      ['name',
                                                                       'id'])
        return products


class WebsiteFormInherit(WebsiteForm):
    """This module extends the functionality of the website form controller
    to handle the creation of new help desk tickets. It provides a new
    controller to display a list of tickets for the current user in their
    portal, and overrides the website form controller's method for handling
    form submissions to create a new help desk ticket instead."""

    def _to_int(self, value):
        try:
            return int(value) if value else False
        except (TypeError, ValueError):
            return False

    def _create_helpdesk_ticket(self, values):
        customer = request.env.user.partner_id
        lowest_stage = request.env['ticket.stage'].sudo().search(
            [], order='sequence, id', limit=1)

        product_ids = []
        products = values.get('product')
        if products:
            product_ids = [
                product_id for product_id in (
                    self._to_int(item) for item in str(products).split(',')
                ) if product_id
            ]

        rec_val = {
            'customer_name': values.get('customer_name'),
            'subject': values.get('subject'),
            'description': values.get('description'),
            'email': values.get('email_from') or customer.email,
            'phone': values.get('phone'),
            'priority': values.get('priority'),
            'customer_id': customer.id,
            'public_ticket': True,
        }
        if lowest_stage:
            rec_val['stage_id'] = lowest_stage.id
        ticket_type_id = self._to_int(values.get('ticket_type'))
        if ticket_type_id:
            rec_val['ticket_type'] = ticket_type_id
        category_id = self._to_int(values.get('category'))
        if category_id:
            rec_val['category_id'] = category_id
        if product_ids:
            rec_val['product_ids'] = [(6, 0, product_ids)]

        ticket = request.env['help.ticket'].sudo().create(rec_val)
        request.session['ticket_number'] = ticket.name
        request.session['ticket_id'] = ticket.id

        attached_files = request.httprequest.files.getlist('ticket_attachment')
        for attachment in attached_files:
            attached_file = attachment.read()
            if not attached_file:
                continue
            request.env['ir.attachment'].sudo().create({
                'name': attachment.filename,
                'res_model': 'help.ticket',
                'res_id': ticket.id,
                'type': 'binary',
                'datas': base64.encodebytes(attached_file),
            })
        return ticket

    @http.route(['/helpdesk_ticket/submit'], type='http', auth="public",
                methods=['POST'], website=True, csrf=False)
    def helpdesk_ticket_submit(self, **post):
        ticket = self._create_helpdesk_ticket(post)
        request.session['form_builder_model_model'] = 'help.ticket'
        request.session['form_builder_model'] = 'Help Ticket'
        request.session['form_builder_id'] = ticket.id
        return request.redirect('/helpdesk_ticket/thanks')

    @http.route(['/helpdesk-thank-you', '/helpdesk_ticket/thanks'],
                type='http', auth="public", website=True, sitemap=False)
    def helpdesk_ticket_thanks(self):
        ticket_id = request.session.get('ticket_id')
        ticket_number = request.session.get('ticket_number') or ''
        ticket_number = html.escape(str(ticket_number))
        if ticket_id and ticket_number:
            ticket_content = (
                f'Your Ticket <a href="/my/tickets/{int(ticket_id)}">'
                f'<strong>{ticket_number}</strong></a> has been registered '
                '<b>successfully</b>'
            )
        elif ticket_number:
            ticket_content = (
                f'Your Ticket <strong>{ticket_number}</strong> has been '
                'registered <b>successfully</b>'
            )
        else:
            ticket_content = 'Your ticket has been registered <b>successfully</b>'

        html_content = f"""
            <html>
                <head>
                    <title>Thank You</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1"/>
                    <link rel="stylesheet" href="/web/assets/1/web.assets_frontend.min.css"/>
                </head>
                <body>
                    <main id="wrap" class="container py-5">
                        <section class="text-center mx-auto" style="max-width: 720px;">
                            <span class="fa fa-4x fa-check-circle text-success mb-3"></span>
                            <h1>Thank You!</h1>
                            <hr class="w-50 mx-auto"/>
                            <h5>{ticket_content}</h5>
                            <p class="mt-3">We will get back to you shortly.</p>
                            <a class="btn btn-primary mt-3" href="/helpdesk_ticket">Create another ticket</a>
                        </section>
                    </main>
                </body>
            </html>
        """
        return request.make_response(html_content)

    def _handle_website_form(self, model_name, **kwargs):
        """Website Help Desk Form"""
        if model_name == 'help.ticket':
            ticket_id = self._create_helpdesk_ticket(kwargs)
            model_record = request.env['ir.model'].sudo().search(
                [('model', '=', model_name)], limit=1)
            request.session['form_builder_model_model'] = model_record.model
            request.session['form_builder_model'] = model_record.name
            request.session['form_builder_id'] = ticket_id.id
            return json.dumps({'id': ticket_id.id})
        else:
            model_record = request.env['ir.model'].sudo().search(
                [('model', '=', model_name)])
            if not model_record:
                return json.dumps({
                    'error': _("The form's specified model does not exist")
                })
            try:
                data = self.extract_data(model_record, request.params)
            # If we encounter an issue while extracting data
            except ValidationError as e:
                return json.dumps({'error_fields': e.args[0]})
            try:
                id_record = self.insert_record(request, model_record,
                                               data['record'], data['custom'],
                                               data.get('meta'))
                if id_record:
                    self.insert_attachment(model_record, id_record,
                                           data['attachments'])
                    # In case of an email, we want to send it immediately instead of waiting
                    # For the email queue to process
                    if model_name == 'mail.mail':
                        request.env[model_name].sudo().browse(id_record).send()

            # Some fields have additional SQL constraints that we can't check generically
            # Ex: crm.lead.probability which is a float between 0 and 1
            # TODO: How to get the name of the erroneous field ?
            except IntegrityError:
                return json.dumps(False)
            request.session['form_builder_model_model'] = model_record.model
            request.session['form_builder_model'] = model_record.name
            request.session['form_builder_id'] = id_record
            return json.dumps({'id': id_record})
