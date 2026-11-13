# LANDRY AI TEAM

Plateforme multi-agents pour la coordination de projets logiciels, organisée autour de LANDRY MANAGER, LANDRY CODER et LANDRY REVIEWER. Cette phase fournit un backend REST sécurisé et persistant. Les bots Telegram et les fournisseurs IA ne sont pas encore intégrés : les conversations et audits sont enregistrés, sans réponse générée automatiquement.

## Architecture

- Backend : Python 3, FastAPI, SQLAlchemy 2, SQLite par défaut, migrations Alembic.
- Authentification : JWT Bearer, mots de passe hachés avec Argon2, rôles `member` et `admin` préparés.
- Frontend : React, TypeScript, Vite et Tailwind CSS (fondation existante).
- Exécution directe sur Linux, Windows et Ubuntu avec venv et npm. **Aucun Docker requis ou fourni.**

## Installation locale

Prérequis : Python 3.10+ et Node.js 18+.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows PowerShell : .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env               # Windows : Copy-Item .env.example .env
```

Configurez une valeur aléatoire forte pour `SECRET_KEY` dans `.env`. Puis appliquez le schéma SQLite :

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

API : http://127.0.0.1:8000 — Swagger/OpenAPI : http://127.0.0.1:8000/docs — OpenAPI JSON : http://127.0.0.1:8000/openapi.json.

Frontend (terminal séparé) :

```bash
cd frontend
npm install
npm run dev
```

## Ubuntu

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
# Installer Node.js 18+ depuis les dépôts adaptés à votre version d'Ubuntu.
git clone https://github.com/landrykayoyo243/landry-ai-team.git
cd landry-ai-team
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Modifier SECRET_KEY dans .env avant un déploiement
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

N'exposez pas le port de développement tel quel sur Internet ; utilisez HTTPS via un reverse proxy, une configuration CORS restrictive et des secrets de production dédiés.

## Authentification et rôles

- `POST /api/v1/auth/register` crée un compte `member`. L'inscription publique ne permet pas de choisir le rôle.
- `POST /api/v1/auth/login` accepte le formulaire OAuth2 `username` (adresse e-mail) et `password`, et renvoie un JWT.
- Swagger : cliquer sur **Authorize** puis utiliser le flux OAuth2 password avec les identifiants.
- Les routes métier requièrent un Bearer token. Un compte utilisateur ne voit/modifie que ses ressources ; les contrôles d'accès administrateur sont prévus dans les dépendances.
- L'attribution du rôle administrateur doit être faite de façon contrôlée côté base de données/opérations d'administration ; aucun endpoint public d'élévation de privilèges n'est exposé.
- Les mots de passe doivent contenir au moins 12 caractères. Les secrets ne sont jamais renvoyés dans les réponses API.

## API REST

Toutes les routes métier sont sous `/api/v1` et détaillées dans Swagger.

| Méthode | Route | Description |
|---|---|---|
| POST | `/auth/register` | Inscription membre |
| POST | `/auth/login` | Connexion et émission JWT |
| GET | `/auth/me` | Profil courant |
| GET | `/agents` | Consulter les trois agents (authentifié) |
| POST / GET | `/projects` | Créer / lister les projets visibles |
| GET / PATCH / DELETE | `/projects/{id}` | Lire, modifier ou supprimer un projet (propriétaire/admin) |
| GET | `/projects/{id}/progress` | Compteurs et pourcentage de tâches terminées |
| POST / GET | `/conversations` | Créer / lister ses conversations |
| POST / GET | `/conversations/{id}/messages` | Enregistrer / récupérer les messages |
| POST / GET | `/projects/{id}/tasks` | Créer / lister les tâches d'un projet |
| PATCH | `/tasks/{id}` | Modifier statut/assignation d'une tâche |
| POST / GET | `/projects/{id}/reviews` | Enregistrer / consulter les audits |

Le premier `alembic upgrade head` crée les sept tables et insère les trois fiches d'agents (Manager, Coder, Reviewer). Une entrée d'agent manquante est également créée lors de la consultation authentifiée de `/agents`.

## Migrations

Créer une migration après modification des modèles :

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

Revenir à la révision précédente : `alembic downgrade -1`. Sauvegardez le fichier SQLite avant toute opération de migration en production.

## Tests

```bash
pytest -q
```

Les tests API utilisent une base SQLite temporaire en mémoire et ne nécessitent aucune clé externe ni Docker.

## Sécurité et limites de cette phase

- `.env` est ignoré par Git ; ne publiez jamais de secrets.
- JWT signé avec `SECRET_KEY`; définissez une clé aléatoire forte et gardez-la privée.
- Accès aux projets/conversations contrôlé par propriétaire, et validation des données par Pydantic.
- CORS autorise uniquement les origines localhost par défaut ; configurez `CORS_ORIGINS` explicitement.
- `GET /api/system` n'expose pas l'URL de base de données ou de configuration secrète.
- Les routes de création de review enregistrent un verdict fourni par l'utilisateur authentifié : ce n'est pas encore un audit automatique par un agent IA.
- Les comptes sont tous membres à l'inscription ; la gestion de comptes admin nécessite une opération hors bande sécurisée.
- Les protections avancées contre abus d'inscription, limitation de débit et rotation/révocation des JWT restent à ajouter avant exposition publique.

## Étapes suivantes

Phase 3 : instructions et comportement des agents. Les intégrations Telegram, IA et GitHub restent hors de cette phase.
