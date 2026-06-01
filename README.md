# Website Helpdesk Support Ticket Management


> Documentation du module Helpdesk web, portail et backend.


## Vue d?ensemble

Ce module permet la cr?ation et le suivi de tickets depuis le site web et le portail client. En backend, les ?quipes support peuvent qualifier les tickets, changer les ?tapes, cr?er des t?ches projet, cr?er des factures de service, fusionner des tickets et r?pondre aux clients.

## Utilisateurs concern?s

- Client/visiteur : cr?e et suit ses tickets via le site ou portail.
- Agent support : traite les tickets et r?pond aux demandes.
- Chef d??quipe helpdesk : configure ?quipes, ?tapes, cat?gories et types.
- Administrateur : configure s?curit?, templates et produits de service.

## Workflow m?tier

1. Cr?ation ticket depuis site ou backend
2. Inbox/Draft
3. In Progress
4. Done
5. Closed
6. Canceled

## Fonctionnement op?rationnel

- Un utilisateur soumet un ticket avec sujet et description.
- Le ticket re?oit une s?quence et une ?tape initiale.
- L?agent affecte ?quipe, priorit? et responsable.
- Cr?er une t?che ou facture si n?cessaire.
- R?pondre depuis le ticket et cl?turer lorsque le traitement est termin?.

## Configuration recommand?e

- Cr?er les ?quipes helpdesk et lier les projets.
- Configurer les ?tapes ticket.
- D?finir cat?gories, types, tags et produits de service.
- V?rifier les templates e-mail et le cron.
- Configurer les droits portail/backend.

## D?pendances Odoo

- `base`
- `website`
- `project`
- `sale_project`
- `hr_timesheet`
- `mail`
- `contacts`

## Mod?les techniques

- `help.team` : Helpdesk Team (`models/help_team.py`)
- `help.ticket` : Help Ticket (`models/help_ticket.py`)
- `helpdesk.categories` : Helpdesk Categories (`models/helpdesk_categories.py`)
- `helpdesk.tag` : Helpdesk Tag (`models/helpdesk_tag.py`)
- `helpdesk.types` : Helpdesk Types (`models/helpdesk_types.py`)
- `merge.tickets` : Merge Tickets (`models/merge_tickets.py`)
- `support_ticket_id` (`models/merge_tickets.py`)
- `support.tickets` : Support Tickets (`models/support_tickets.py`)
- `ticket.stage` : Ticket Stage (`models/ticket_stage.py`)
- `fold` (`models/ticket_stage.py`)

## ?tats d?tect?s dans le code

- `models/help_ticket.py` : `normal` (Ready), `done` (In Progress), `blocked` (Blocked)

## Actions serveur principales

- `action_create_invoice` (`models/help_ticket.py`)
- `action_create_tasks` (`models/help_ticket.py`)
- `action_open_tasks` (`models/help_ticket.py`)
- `action_open_invoices` (`models/help_ticket.py`)
- `action_open_merged_tickets` (`models/help_ticket.py`)
- `action_send_reply` (`models/help_ticket.py`)
- `action_merge_ticket` (`models/merge_tickets.py`)

## Fichiers charg?s par le manifest

- `security/odoo_website_helpdesk_security.xml`
- `security/ir.model.access.csv`
- `data/ir_sequence_data.xml`
- `data/ticket_stage_data.xml`
- `data/mail_template.xml`
- `data/helpdesk_types_data.xml`
- `data/ir_cron_data.xml`
- `data/mail_template_data.xml`
- `views/help_team_views.xml`
- `views/portal_search_templates.xml`
- `views/res_config_settings_views.xml`
- `views/website_form.xml`
- `views/report_templates.xml`
- `views/help_ticket_views.xml`
- `views/portal_views_templates.xml`
- `views/helpdesk_categories_views.xml`
- `views/rating_form_templates.xml`
- `views/merge_tickets_views.xml`
- `views/helpdesk_tag_views.xml`
- `views/helpdesk_types_views.xml`
- `views/ticket_stage_views.xml`
- `views/helpdesk_replay_template.xml`
- `views/odoo_website_helpdesk_menus.xml`
- `report/help_ticket_templates.xml`

## S?curit? et droits

Le module s?appuie sur les fichiers suivants pour d?finir les groupes, r?gles d?enregistrement et droits d?acc?s :

- `security/ir.model.access.csv`
- `security/odoo_website_helpdesk_security.xml`

## Rapports

- `report/help_ticket_templates.xml`

## Assets et interface

- `static/src/cdn/docs/javascripts/jquery.sumoselect.min.js`
- `static/src/cdn/docs/javascripts/main.js`
- `static/src/cdn/docs/stylesheets/print.css`
- `static/src/cdn/docs/stylesheets/pygment_trac.css`
- `static/src/cdn/docs/stylesheets/stylesheet.css`
- `static/src/cdn/docs/stylesheets/sumoselect.min.css`
- `static/src/cdn/gpr-hack.js`
- `static/src/cdn/jquery.sumoselect.js`
- `static/src/cdn/jquery.sumoselect.min.js`
- `static/src/cdn/sumoselect.css`
- `static/src/cdn/sumoselect.min.css`
- `static/src/js/helpdesk_dashboard_action.js`
- `static/src/js/helpdesk_sale_error_guard.js`
- `static/src/js/helpdesk_ticket_submit.js`
- `static/src/js/multiple_product_choose.js`
- `static/src/js/portal_groupby_and_search.js`
- `static/src/js/ticket_details.js`
- `static/src/scss/rating.css`
- `static/src/xml/help_ticket_templates.xml`

## Bonnes pratiques d?utilisation

- V?rifier que chaque utilisateur Odoo est li? au bon employ? lorsque le module d?pend de `hr.employee`.
- Tester le workflow avec un dossier de test avant utilisation en production.
- Contr?ler les groupes de s?curit? apr?s installation afin que seuls les bons r?les voient les boutons de validation.
- Garder les templates e-mail et rapports align?s avec les proc?dures internes.
- Sauvegarder la base avant toute modification structurelle du module.

## Maintenance

- Les ?volutions fonctionnelles doivent ?tre ajout?es dans les mod?les Python, les vues XML et les r?gles de s?curit? correspondantes.
- Apr?s modification des vues, mettre ? jour le module depuis Odoo ou red?marrer le serveur selon le type de changement.
- Apr?s modification des assets, vider le cache navigateur et recompiler les assets si n?cessaire.
- Toute nouvelle ?tape de workflow doit ?tre accompagn?e des droits, boutons, notifications et filtres correspondants.
