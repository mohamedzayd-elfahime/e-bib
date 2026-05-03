# e-bib

Application web de bibliotheque construite avec FastAPI, Jinja2, SQLAlchemy et MySQL.

Le projet est encore en cours de developpement, mais il contient deja les bases d'une application de gestion de bibliotheque : authentification, consultation des livres, favoris, emprunts, reservations, retours, avis et notifications WebSocket.

## Prerequis

- Python 3.11 ou plus recent
- MySQL

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copier le fichier d'exemple de configuration :

```bash
copy .env.example .env
```

Puis modifier `.env` avec les informations de votre base de donnees et vos secrets locaux.

## Lancement

```bash
uvicorn app.main:app --reload
```

L'application sera disponible sur `http://localhost:8000`.

## Tests

```bash
pytest
```

## Notes de securite

Le fichier `.env` ne doit pas etre publie. Utilisez `.env.example` pour documenter les variables attendues sans exposer les vrais secrets.
