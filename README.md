# e-bib

e-bib est une application web de gestion de bibliotheque construite avec FastAPI.
Le projet est encore en cours de developpement, mais il met deja en place une base solide pour une application complete : authentification, consultation du catalogue, emprunts, reservations, retours, favoris, avis utilisateurs et notifications.

L'objectif du projet est de travailler sur une application proche d'un cas reel, avec une architecture claire, une separation des responsabilites et une logique metier testable.

## Ce que le projet demontre

- Conception d'une application web avec FastAPI, Jinja2, SQLAlchemy et MySQL.
- Organisation du code en couches inspiree de la Clean Architecture.
- Separation entre domaine, cas d'utilisation, infrastructure et presentation.
- Conception UML avant et pendant l'implementation : cas d'utilisation, activites, etats-transitions et classes.
- Authentification avec JWT, gestion des sessions et protection CSRF.
- Modelisation de regles metier autour des emprunts, reservations, retours et disponibilites.
- Utilisation de repositories pour isoler l'acces aux donnees.
- Ajout de tests unitaires avec Pytest.
- Configuration securisee via variables d'environnement.

## Fonctionnalites principales

- Connexion utilisateur avec generation de tokens JWT.
- Connexion via Google OAuth.
- Consultation des livres et details d'un livre.
- Filtrage et recherche dans le catalogue.
- Gestion des favoris.
- Reservation de livres.
- Emprunt et retour de livres.
- Ajout et consultation des avis utilisateurs.
- Notifications liees aux evenements de la bibliotheque.
- WebSocket pour les notifications en temps reel.
- Page de profil utilisateur.

## Architecture

Le projet est organise pour eviter de melanger la logique metier avec les details techniques.

```text
app/
  domain/           Entites, evenements et services metier
  application/      Cas d'utilisation, DTO, ports et politiques applicatives
  infrastructure/   Base de donnees, repositories, securite, event bus
  presentation/     Routes FastAPI, templates, fichiers statiques, WebSocket
  config.py         Chargement de la configuration
  main.py           Point d'entree de l'application
tests/              Tests unitaires et tests d'integration
docs/uml/           Diagrammes UML et documents de conception
```

Cette structure permet de faire evoluer le projet plus facilement : la logique metier reste independante de FastAPI, de MySQL ou des details d'interface.

## Conception UML

Le projet est accompagne de diagrammes UML pour documenter l'analyse et la conception.
Ces diagrammes montrent les parcours utilisateurs, les traitements principaux et la structure globale du domaine.

- [Diagramme de cas d'utilisation](docs/uml/use-case-diagram.svg)
- [Diagramme de classes](docs/uml/class-diagram.drawio.html)
- [Diagramme etats-transitions](docs/uml/state-transition-diagram.drawio.html)
- [Activite - authentification](docs/uml/activity-authentification.svg)
- [Activite - recherche de livres](docs/uml/activity-search.svg)
- [Activite - details d'un livre](docs/uml/activity-book-details.svg)
- [Activite - emprunt](docs/uml/activity-borrow-book.svg)
- [Activite - reservation](docs/uml/activity-reservation.svg)
- [Activite - retour de livre](docs/uml/activity-return-book.svg)
- [Activite - prolongation](docs/uml/activity-renew-loan.svg)
- [Activite - avis utilisateur](docs/uml/activity-review.svg)
- [Activite - favoris](docs/uml/activity-toggle-favorite.svg)

## Stack technique

- Python 3.11+
- FastAPI
- Jinja2
- SQLAlchemy
- MySQL / PyMySQL
- JWT avec `python-jose`
- Argon2 pour le hachage des mots de passe
- Sessions Starlette
- WebSocket
- Pytest

## Securite

Le projet utilise une configuration basee sur des variables d'environnement. Le fichier `.env` local n'est pas versionne.

Un fichier `.env.example` est fourni pour documenter les variables necessaires sans exposer de secrets.

Elements deja pris en compte :

- secrets JWT via variables d'environnement
- secret de session via variables d'environnement
- hachage des mots de passe avec Argon2
- protection CSRF
- separation entre configuration locale et code source
- exclusion des fichiers sensibles avec `.gitignore`

## Installation

Creer un environnement virtuel :

```bash
python -m venv .venv
```

Activer l'environnement virtuel sous Windows :

```bash
.venv\Scripts\activate
```

Installer les dependances :

```bash
pip install -r requirements.txt
```

Creer le fichier de configuration local :

```bash
copy .env.example .env
```

Modifier ensuite `.env` avec les informations de votre base MySQL et vos secrets locaux.

## Lancement

```bash
uvicorn app.main:app --reload
```

L'application sera disponible sur :

```text
http://localhost:8000
```

## Tests

```bash
pytest
```

Etat actuel des tests :

```text
7 passed
```

## Etat du projet

Le projet est un travail en cours. Certaines parties peuvent encore etre ameliorees ou completees, notamment la couverture de tests, l'experience utilisateur, la documentation API et le deploiement.

Malgre cela, le projet presente deja une base technique representative d'une application backend/web structuree, avec de vraies decisions d'architecture, de securite et de logique metier.

## Axes d'amelioration prevus

- Ajouter des migrations de base de donnees.
- Completer les tests d'integration.
- Ameliorer l'interface utilisateur.
- Ajouter une documentation API plus detaillee.
- Preparer un deploiement Docker.
- Ajouter des roles utilisateurs plus avances.

## Auteur

Projet personnel realise pour pratiquer la conception d'applications web avec FastAPI, architecture en couches, securite applicative et logique metier.
