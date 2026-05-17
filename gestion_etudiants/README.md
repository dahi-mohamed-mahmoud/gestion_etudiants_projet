# 🎓 GestEtudiant — Plateforme de Gestion des Étudiants

![CI/CD](https://github.com/dahi-mohamed-mahmoud/gestion-etudiants/actions/workflows/ci-cd.yml/badge.svg)
![Docker](https://img.shields.io/docker/pulls/VOTRE_USERNAME/gestion-etudiants)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-5.0-green)

> Mini-projet DevOps — Module DevOps 2025-2026  
> Pr. Soufiane HAMIDA

---

## 📋 Description

GestEtudiant est une application web Django permettant la gestion complète des étudiants : inscription, consultation, mise à jour des fiches, gestion des notes et export des relevés. Elle intègre une authentification par rôle via Django Admin.

## ✨ Fonctionnalités

- ✅ CRUD complet des étudiants (créer, lire, modifier, supprimer)
- ✅ Gestion des filières, matières et niveaux
- ✅ Saisie et consultation des notes par matière et session
- ✅ Calcul automatique de la moyenne générale
- ✅ Export des relevés de notes en CSV
- ✅ Recherche et filtrage multi-critères
- ✅ Authentification sécurisée (admin Django)
- ✅ Interface responsive Bootstrap 5

## 🛠️ Stack technique

| Composant | Technologie |
|-----------|-------------|
| Backend | Django 5.0 (Python 3.12) |
| Base de données | PostgreSQL 16 |
| Frontend | HTML5 + Bootstrap 5 + Bootstrap Icons |
| Serveur WSGI | Gunicorn |
| Conteneurisation | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Registre | Docker Hub |

## 🚀 Démarrage rapide (Docker)

```bash
# 1. Cloner le dépôt
git clone https://github.com/VOTRE_USERNAME/gestion-etudiants.git
cd gestion-etudiants

# 2. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos valeurs

# 3. Lancer toute la stack
docker compose up --build

# 4. Créer le super-utilisateur admin
docker compose exec web python manage.py createsuperuser

# 5. Accéder à l'application
# → http://localhost:8000
# → http://localhost:8000/admin
```

## 🔧 Développement local (sans Docker)

```bash
# Prérequis : Python 3.12, PostgreSQL

python -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate
pip install -r requirements.txt

# Configurer les variables d'environnement
export POSTGRES_HOST=localhost
export POSTGRES_DB=gestion_etudiants
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export SECRET_KEY=ma-cle-secrete
export DEBUG=True

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 🧪 Lancer les tests

```bash
# Tests unitaires et d'intégration
python manage.py test students --verbosity=2

# Avec couverture de code
pip install coverage
coverage run manage.py test students
coverage report
```

## 🔍 Lint

```bash
flake8 . --max-line-length=120 --exclude=migrations
```

## 🐳 Image Docker

```bash
# Construire localement
docker build -t gestion-etudiants .

# Depuis Docker Hub
docker pull VOTRE_USERNAME/gestion-etudiants:latest
```

## ⚙️ Variables d'environnement

| Variable | Description | Défaut |
|----------|-------------|--------|
| `SECRET_KEY` | Clé secrète Django | (obligatoire en prod) |
| `DEBUG` | Mode debug | `True` |
| `ALLOWED_HOSTS` | Hôtes autorisés | `localhost 127.0.0.1` |
| `POSTGRES_DB` | Nom de la base | `gestion_etudiants` |
| `POSTGRES_USER` | Utilisateur PostgreSQL | `postgres` |
| `POSTGRES_PASSWORD` | Mot de passe PostgreSQL | `postgres` |
| `POSTGRES_HOST` | Hôte PostgreSQL | `db` |
| `POSTGRES_PORT` | Port PostgreSQL | `5432` |

## 🔄 Pipeline CI/CD

Le pipeline GitHub Actions se déclenche à chaque push et PR :

```
push/PR
  └─► 🧪 Lint (flake8) + Tests Django
        └─► 🐳 Build image Docker
              └─► 🚀 Push Docker Hub (main uniquement)
```

**Secrets GitHub à configurer :**
- `DOCKERHUB_USERNAME` : votre nom d'utilisateur Docker Hub
- `DOCKERHUB_TOKEN` : token d'accès Docker Hub

## 📁 Structure du projet

```
gestion_etudiants/
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # Pipeline GitHub Actions
├── gestion_etudiants/
│   ├── settings.py             # Configuration Django
│   ├── urls.py                 # Routes principales
│   └── wsgi.py
├── students/
│   ├── migrations/             # Migrations BDD
│   ├── templates/students/     # Templates HTML
│   ├── admin.py                # Configuration admin
│   ├── apps.py
│   ├── forms.py                # Formulaires
│   ├── models.py               # Modèles (Etudiant, Filiere, Note...)
│   ├── tests.py                # Tests unitaires & intégration
│   ├── urls.py                 # Routes de l'app
│   └── views.py                # Vues
├── .env.example                # Template variables d'environnement
├── .gitignore
├── docker-compose.yml          # Stack complète
├── Dockerfile                  # Multi-stage build
├── manage.py
├── README.md
└── requirements.txt
```

## 👥 Auteurs

- **Cheikh ahmed Mohamed abdallahi** — [GitHub](https://github.com/Mohamed-Abdallahi)
- **Mohamed mahmoud Dahi** — [GitHub](https://github.com/dahi-mohamed-mahmoud)

---

*Projet réalisé dans le cadre du module DevOps — 2025-2026*
