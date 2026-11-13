# LANDRY AI TEAM

LANDRY AI TEAM est une plateforme multi-agents IA pour la coordination de projets logiciels, avec trois rôles indépendants : LANDRY MANAGER, LANDRY CODER et LANDRY REVIEWER.

## Vue d'ensemble

- Backend FastAPI en Python 3
- Frontend React + TypeScript + Vite + Tailwind CSS
- Base SQLite par défaut pour le démarrage rapide
- Intégrations configurables : Telegram, GitHub, providers IA
- Sécurité : `.env` local, validation des variables, autorisations Telegram, confirmation humaine avant les actions sensibles
- Sans Docker : exécution directe sur Linux, Windows ou Ubuntu

## Architecture proposée

```text
landry-ai-team/
├── app/
│   ├── agents/
│   ├── api/
│   ├── services/
│   ├── database/
│   ├── config.py
│   └── main.py
├── frontend/
├── tests/
├── docs/
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── package.json (dans frontend)
```

## Prérequis

- Python 3.10+
- Node.js 18+
- npm
- Git
- Un accès shell local ou distant

## Installation backend

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Installation frontend

```bash
cd frontend
npm install
npm run dev
```

## Installation sur Ubuntu

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nodejs npm git
cd /path/to/landry-ai-team
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Dans un second terminal :

```bash
cd /path/to/landry-ai-team/frontend
npm install
npm run dev
```

## Variables d'environnement

Copiez le modèle et configurez les valeurs locales :

```bash
cp .env.example .env
```

Ne jamais commiter le fichier `.env` réel.

## Sécurité

- Aucune clé secrète dans le code
- Utilisation de `.env` non suivi par Git
- Vérification des tokens Telegram
- Accès utilisateur restreint
- Aucune exécution avec privilèges root ou administrateur
- Confirmation humaine pour opérations destructrices ou déploiements

## Workflow logiciel

1. L'utilisateur dialogue avec MANAGER
2. MANAGER clarifie le besoin
3. MANAGER prépare le cahier des charges
4. L'utilisateur valide
5. CODER développe
6. REVIEWER audite
7. CODER applique les corrections si nécessaire
8. MANAGER présente le résultat final

## Développement progressif

- Phase 1 : Structure et architecture
- Phase 2 : Backend et base de données
- Phase 3 : Trois agents IA
- Phase 4 : Orchestration
- Phase 5 : Intégration Telegram
- Phase 6 : Intégration IA
- Phase 7 : Intégration GitHub
- Phase 8 : Dashboard React
- Phase 9 : Tests et documentation

## Tests réalisés dans cette étape

- Vérification des permissions GitHub
- Vérification que le dépôt est vide et prêt pour l'initialisation
- Création de la structure de base sans Docker
- Validation de l'application Python de base via import et test de santé

## Prochaines étapes

1. Implémenter les modèles de base de données SQLAlchemy
2. Ajouter les endpoints API du manager/coder/reviewer
3. Créer les agents avec instructions métier
4. Ajouter l'intégration Telegram webhook
5. Connecter les fournisseurs de modèles AI
6. Construire le dashboard React et les vues d'administration
7. Ajouter les tests automatisés complets

## Remarques

Le dépôt était initialement vide. Cette première étape a donc posé les fondations du projet, sans Docker, conformément aux exigences.
