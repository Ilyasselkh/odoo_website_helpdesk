# Website Helpdesk Support Ticket Management

Module Odoo Helpdesk pour creer des tickets depuis le site web, les suivre depuis le portail et les traiter en backend avec equipes, etapes, priorites, taches, factures et reponses client.

## Objectif

Cette documentation explique le perimetre fonctionnel du module, les roles utilisateurs, le workflow, la configuration et les principaux objets techniques.

## Utilisateurs concernes

- Client ou visiteur
- Agent support
- Chef equipe helpdesk
- Administrateur Odoo

## Workflow metier

1. Creation ticket
2. Inbox ou Draft
3. In Progress
4. Done
5. Closed
6. Canceled

## Fonctionnement operationnel

- Soumettre un ticket depuis le site.
- Qualifier le ticket en backend.
- Affecter equipe, priorite et responsable.
- Creer une tache ou facture si besoin.
- Repondre au client.
- Cloturer ou annuler le ticket.

## Configuration recommandee

- Creer les equipes helpdesk.
- Configurer les etapes ticket.
- Definir categories, types, tags et produits service.
- Verifier templates mail et cron.
- Configurer acces portail et backend.

## Dependances Odoo

- `base`
- `mail`
- `website`
- `project`
- `sale_project`
- `hr_timesheet`
- `contacts`

## Modeles principaux

- `help.ticket`
- `help.team`
- `ticket.stage`
- `helpdesk.categories`
- `helpdesk.types`
- `helpdesk.tag`
- `merge.tickets`
- `support.tickets`

## Structure importante du module

- `security/ir.model.access.csv`
- `security/odoo_website_helpdesk_security.xml`
- `data/helpdesk_types_data.xml`
- `data/ir_cron_data.xml`
- `data/ir_sequence_data.xml`
- `data/mail_template.xml`
- `data/mail_template_data.xml`
- `data/ticket_stage_data.xml`
- `views/help_team_views.xml`
- `views/help_ticket_views.xml`
- `views/helpdesk_categories_views.xml`
- `views/helpdesk_replay_template.xml`
- `views/helpdesk_tag_views.xml`
- `views/helpdesk_types_views.xml`
- `views/merge_tickets_views.xml`
- `views/odoo_website_helpdesk_menus.xml`
- `views/portal_search_templates.xml`
- `views/portal_views_templates.xml`
- `views/rating_form_templates.xml`
- `views/report_templates.xml`
- `views/res_config_settings_views.xml`
- `views/ticket_stage_views.xml`
- `views/website_form.xml`
- `report/help_ticket_templates.xml`
- `models/__init__.py`
- `models/account_move.py`
- `models/help_team.py`
- `models/help_ticket.py`
- `models/helpdesk_categories.py`
- `models/helpdesk_tag.py`
- `models/helpdesk_types.py`
- `models/ir_actions_cleanup.py`
- `models/mail_compose_message.py`
- `models/merge_tickets.py`
- `models/project_task.py`
- `models/res_config_settings.py`
- `models/support_tickets.py`
- `models/ticket_stage.py`
- `models/website_menu.py`

## Securite

Les droits sont geres par les fichiers du dossier `security`. Il faut verifier les groupes, les regles enregistrement et les acces CSV apres installation ou modification du module.

## Notifications et suivi

Les modules qui dependent de `mail` utilisent le chatter Odoo pour tracer les changements. Les templates mail presents dans le dossier `data` servent a notifier les acteurs concernes par les transitions.

## Installation

1. Copier le module dans le dossier addons Odoo.
2. Redemarrer le serveur Odoo si necessaire.
3. Mettre a jour la liste des applications.
4. Installer ou mettre a jour le module.
5. Verifier les droits utilisateurs et tester un dossier de bout en bout.

## Maintenance

- Ajouter toute nouvelle etape a la fois dans le modele Python, les vues XML, les droits et les notifications.
- Tester les workflows avec plusieurs roles utilisateurs.
- Mettre a jour les rapports et templates mail quand la procedure interne change.
- Eviter de modifier les donnees de production sans sauvegarde.
- Documenter toute evolution fonctionnelle dans ce README.
