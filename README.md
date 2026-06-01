# Website Helpdesk Support Ticket Management

Module Odoo de gestion de tickets helpdesk depuis le site web, le portail et le backend.

## Objectif

Ce module permet aux clients ou utilisateurs de créer des tickets support depuis le site web, de les suivre depuis le portail et de les traiter en backend avec équipes, étapes, priorités, tâches, factures et réponses.

## Dépendances

- `base`
- `website`
- `project`
- `sale_project`
- `hr_timesheet`
- `mail`
- `contacts`

## Modèles principaux

- `help.ticket` : ticket support.
- `help.team` : équipe helpdesk.
- `ticket.stage` : étapes du workflow ticket.
- `helpdesk.categories` : catégories.
- `helpdesk.types` : types.
- `helpdesk.tag` : tags.
- `merge.tickets` : fusion de tickets.
- `support.tickets` : configuration/affichage support.

## Workflow ticket

Le ticket est créé avec une séquence, un client, un sujet, une description, une priorité, une équipe et une étape. Les étapes standard incluent notamment Inbox, Draft, In Progress, Done, Closed et Canceled. Les changements d'étape peuvent déclencher des notifications et du suivi dans le chatter.

## Fonctionnement

- Création de ticket depuis le site web.
- Consultation et recherche depuis le portail.
- Affectation à une équipe et à un utilisateur.
- Gestion de priorité, tags, catégorie et type.
- Création de tâches projet depuis un ticket.
- Création de factures de service.
- Ouverture des tâches, factures et tickets fusionnés.
- Réponse au client depuis le ticket.
- Fusion de tickets liés.

## Portail et site web

Le module ajoute des contrôleurs web et portail pour la création, la recherche, le groupement et le détail des tickets. Des templates frontend permettent la saisie et le suivi côté client.

## Données chargées

- Séquences ticket.
- Étapes ticket.
- Types helpdesk.
- Templates e-mail.
- Cron de traitement.

## Sécurité

Les droits et groupes sont définis dans :

- `security/odoo_website_helpdesk_security.xml`
- `security/ir.model.access.csv`

## Assets

Le module charge des scripts backend, frontend et templates XML pour le dashboard, le portail, la soumission de tickets et les protections de saisie.

