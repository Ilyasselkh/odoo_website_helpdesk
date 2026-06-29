# Website Helpdesk Support Ticket Management

Module Odoo de gestion des tickets support depuis le site web et le backend.

Le module permet aux clients ou utilisateurs portail de creer des tickets depuis le site, puis aux equipes support de les traiter dans Odoo avec stages, categories, tags, equipes, temps passe, taches projet, facturation et notifications.

## Objectif fonctionnel

Centraliser le support client dans Odoo et relier les tickets aux processus projet, vente, temps passe et facturation.

Le module permet de :

- creer des tickets depuis le site web ;
- gerer les tickets depuis le backend ;
- organiser les tickets par equipe ;
- classer les tickets par type, categorie et tags ;
- utiliser des stages de traitement ;
- notifier les acteurs lors des changements d'etape ;
- repondre au client ;
- fusionner des tickets ;
- creer des taches projet depuis un ticket ;
- suivre le temps passe ;
- creer des factures de service ;
- afficher les tickets dans le portail ;
- collecter une evaluation ou un retour client.

## Roles fonctionnels

### Client / utilisateur portail

Le client cree et suit ses tickets.

Il peut :

- soumettre un ticket depuis le site ;
- renseigner le sujet, la description et les informations de contact ;
- consulter ses tickets dans le portail ;
- repondre aux messages ;
- evaluer le support selon la configuration.

### Agent support

L'agent support traite les tickets au quotidien.

Il peut :

- consulter les tickets ;
- changer le stage ;
- repondre au client ;
- affecter une equipe ;
- ajouter des tags ;
- creer une tache ;
- saisir du temps ;
- fermer ou annuler un ticket.

### Responsable helpdesk

Le responsable helpdesk gere l'organisation du support.

Il peut :

- configurer les equipes ;
- configurer les stages ;
- suivre les tickets ouverts et fermes ;
- fusionner des tickets ;
- verifier les notifications ;
- suivre les indicateurs de traitement.

### Administrateur

L'administrateur gere les parametres, les droits, les menus web et les integrations.

## Stages des tickets

Les stages sont configurables dans le modele `ticket.stage`.

Le module utilise notamment les notions suivantes :

- stage de depart ;
- stage ferme ;
- stage annule ;
- stage replie en Kanban ;
- sequence d'affichage.

Les stages courants incluent :

- `Inbox`
- `Draft`
- `In Progress`
- `Done`
- `Closed`
- `Canceled`

## Flux standard

1. Creation du ticket depuis le site ou le backend.
2. Arrivee dans le stage initial.
3. Qualification par type, categorie, equipe et tags.
4. Traitement par l'agent support.
5. Reponse au client.
6. Creation de tache ou facture si necessaire.
7. Passage en stage ferme ou annule.
8. Suivi portail et evaluation.

## Creation depuis le site web

Le module fournit des templates website pour afficher le formulaire de ticket et les pages portail.

Les assets frontend gerent notamment la soumission du ticket et certaines protections JavaScript.

## Notifications

Le module envoie des emails lors des changements de stage.

Les destinataires peuvent dependre de l'etape :

- client ;
- equipe support ;
- utilisateurs internes ;
- contacts lies au ticket.

Fichiers principaux :

- `data/mail_template.xml`
- `data/mail_template_data.xml`

## Taches, temps passe et facturation

Le module est integre avec :

- `project`
- `sale_project`
- `hr_timesheet`
- `account`

Fonctionnalites principales :

- creation de taches depuis le ticket ;
- ouverture des taches liees ;
- creation de factures ;
- ouverture des factures liees ;
- suivi du temps passe selon la configuration.

## Fusion de tickets

Le modele `merge.tickets` permet de fusionner des tickets ou de rattacher des tickets proches.

Cette fonction evite les doublons lorsqu'un meme sujet est remonte plusieurs fois.

## Parametrage

Les parametres importants incluent :

- stage de fermeture ;
- equipes helpdesk ;
- categories ;
- types ;
- tags ;
- templates email ;
- menus website et portail.

## Modeles principaux

- `help.ticket`
- `help.team`
- `ticket.stage`
- `helpdesk.categories`
- `helpdesk.types`
- `helpdesk.tag`
- `support.tickets`
- `merge.tickets`

## Structure du module

- `security/odoo_website_helpdesk_security.xml`
- `security/ir.model.access.csv`
- `data/ir_sequence_data.xml`
- `data/ticket_stage_data.xml`
- `data/helpdesk_types_data.xml`
- `data/mail_template.xml`
- `data/mail_template_data.xml`
- `data/ir_cron_data.xml`
- `views/help_ticket_views.xml`
- `views/help_team_views.xml`
- `views/ticket_stage_views.xml`
- `views/helpdesk_categories_views.xml`
- `views/helpdesk_types_views.xml`
- `views/helpdesk_tag_views.xml`
- `views/website_form.xml`
- `views/portal_views_templates.xml`
- `views/portal_search_templates.xml`
- `views/res_config_settings_views.xml`
- `views/merge_tickets_views.xml`
- `report/help_ticket_templates.xml`
- `models/help_ticket.py`
- `models/help_team.py`
- `models/ticket_stage.py`
- `models/merge_tickets.py`

## Installation

1. Copier le module dans le dossier addons Odoo.
2. Verifier les dependances Odoo : website, project, sale_project, hr_timesheet, mail et contacts.
3. Redemarrer le serveur Odoo si necessaire.
4. Mettre a jour la liste des applications.
5. Installer le module.
6. Configurer les stages et le stage de fermeture.
7. Configurer les equipes support.
8. Tester la creation d'un ticket depuis le site.
9. Tester un changement de stage et la notification email.

## Maintenance fonctionnelle

Lorsqu'une regle support change, verifier aussi :

- les stages ;
- les templates email ;
- le formulaire website ;
- les droits portail ;
- les integrations projet/facturation ;
- les actions de fusion ;
- ce README.
