# 📚 ELECAM API — Documentation Complète

> **Backend Django REST Framework** pour la gestion des élections au Cameroun.  
> Version : `v3` | Framework : Django 6.0.3 + DRF 3.16.1

---

## 🗂️ Table des matières

| Section | Fichier |
|---------|---------|
| 🔐 Authentification & Utilisateurs | [auth.md](./auth.md) |
| 🗳️ Élections & Types d'élection | [elections.md](./elections.md) |
| 👤 Candidats & Résultats | [candidates.md](./candidates.md) |
| 📊 Statistiques & Géographie | [statistics.md](./statistics.md) |
| 📅 Calendrier, Bureaux & Points de retrait | [infrastructure.md](./infrastructure.md) |

---

## 🚀 Présentation générale

L'API ELECAM est une API REST sécurisée permettant de :
- Gérer les **utilisateurs** et l'**authentification JWT**
- Consulter et administrer les **élections** (types, candidats, résultats)
- Accéder aux **statistiques électorales** (national, régional, départemental, diaspora)
- Gérer la **géographie électorale** (régions, départements)
- Suivre le **calendrier électoral**
- Localiser les **bureaux de vote** et **points de retrait**

---

## 🌐 URL de base

```
https://<votre-domaine>/api/
```

### Health Check
```http
GET /api/health-check/
```
Réponse : `200 OK` — vérifie que l'API est en ligne.

---

## 🔑 Authentification

L'API utilise **JWT (JSON Web Tokens)** via `djangorestframework-simplejwt`.

### Durée de vie des tokens

| Rôle | Access Token | Refresh Token |
|------|-------------|---------------|
| Utilisateur normal | 2 heures | — |
| Administrateur | 24 heures | Oui (rotation) |

### Comment utiliser le token

Ajouter le header suivant à chaque requête protégée :

```http
Authorization: Bearer <access_token>
```

---

## 📋 Vue d'ensemble des endpoints

### 🔐 Authentification (`/api/auth/`)
| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| POST | `/api/auth/register/` | Inscription | ❌ |
| POST | `/api/auth/login/` | Connexion | ❌ |
| POST | `/api/auth/logout/` | Déconnexion | ✅ |
| POST | `/api/auth/token/refresh/` | Rafraîchir le token | ❌ |
| GET | `/api/auth/profile/` | Voir son profil | ✅ |
| PUT/PATCH | `/api/auth/profile/update/` | Modifier son profil | ✅ |
| DELETE | `/api/auth/profile/delete/` | Supprimer son compte | ✅ |
| POST | `/api/auth/change-password/` | Changer de mot de passe | ✅ |
| GET | `/api/auth/count/` | Nombre d'utilisateurs | ❌ |
| POST | `/api/auth/password-reset/request/` | Demander reset MDP | ❌ |
| POST | `/api/auth/password-reset/verify/` | Vérifier code reset | ❌ |
| POST | `/api/auth/password-reset/confirm/` | Confirmer reset MDP | ❌ |

### 🗳️ Élections (`/api/elections/`)
| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| GET | `/api/elections/elections/` | Liste des élections | ❌ |
| POST | `/api/elections/elections/` | Créer une élection | 🔒 Admin |
| GET | `/api/elections/elections/{id}/` | Détail d'une élection | ❌ |
| PUT/PATCH | `/api/elections/elections/{id}/` | Modifier une élection | 🔒 Admin |
| DELETE | `/api/elections/elections/{id}/` | Supprimer une élection | 🔒 Admin |
| GET | `/api/elections/elections/statistics/` | Statistiques globales | ❌ |

### 📂 Types d'élection (`/api/election-types/`)
| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| GET | `/api/election-types/` | Liste des types | ❌ |
| POST | `/api/election-types/` | Créer un type | 🔒 Admin |
| GET | `/api/election-types/{id}/` | Détail d'un type | ❌ |
| PUT/PATCH | `/api/election-types/{id}/` | Modifier un type | 🔒 Admin |
| DELETE | `/api/election-types/{id}/` | Supprimer un type | 🔒 Admin |

### 👤 Candidats (`/api/candidates/`)
| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| GET | `/api/candidates/` | Liste des candidats | ❌ |
| POST | `/api/candidates/` | Créer un candidat | 🔒 Admin |
| GET | `/api/candidates/{id}/` | Détail d'un candidat | ❌ |
| PUT/PATCH | `/api/candidates/{id}/` | Modifier un candidat | 🔒 Admin |
| DELETE | `/api/candidates/{id}/` | Supprimer un candidat | 🔒 Admin |

### 🏆 Résultats candidats (`/api/candidate-results/`)
| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| GET | `/api/candidate-results/global/` | Résultats globaux | ❌ |
| GET | `/api/candidate-results/global/podium/` | Top 3 candidats | ❌ |
| GET | `/api/candidate-results/global/winner/` | Vainqueur | ❌ |
| GET | `/api/candidate-results/regional/` | Résultats par région | ❌ |
| GET | `/api/candidate-results/departmental/` | Résultats par département | ❌ |
| GET | `/api/candidate-results/diaspora/` | Résultats diaspora | ❌ |
| GET | `/api/candidate-results/diaspora/ranking/` | Classement diaspora | ❌ |

### 🗺️ Géographie
| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| GET | `/api/regions/` | Liste des régions | ❌ |
| GET | `/api/regions/{id}/` | Détail d'une région | ❌ |
| GET | `/api/departments/` | Liste des départements | ❌ |
| GET | `/api/departments/{id}/` | Détail d'un département | ❌ |
| GET | `/api/departments/by-region/{region_id}/` | Départements par région | ❌ |

### 🎖️ Partis politiques (`/api/political-parties/`)
| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| GET | `/api/political-parties/` | Liste des partis | ❌ |
| POST | `/api/political-parties/` | Créer un parti | 🔒 Admin |
| GET | `/api/political-parties/{id}/` | Détail d'un parti | ❌ |

### 📊 Statistiques
| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| GET | `/api/voter-statistics/` | Stats électeurs globales | ❌ |
| GET | `/api/department-stats/` | Stats par département | ❌ |
| GET | `/api/department-stats/by-region/` | Stats depts groupées par région | ❌ |
| GET | `/api/region-stats/` | Stats par région | ❌ |
| GET | `/api/region-stats/by-type/` | Stats régions (nat. vs diaspora) | ❌ |
| GET | `/api/diaspora-stats/` | Stats diaspora | ❌ |
| GET | `/api/diaspora-stats/aggregate/` | Agrégat diaspora | ❌ |

### 📅 Infrastructure
| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| GET | `/api/calendrier-electoral/` | Calendrier électoral | ❌ |
| GET | `/api/calendrier-electoral/upcoming/` | Prochains événements | ❌ |
| GET | `/api/voting-offices/` | Bureaux de vote | ❌ |
| GET | `/api/pickup-points/` | Points de retrait | ❌ |

---

## ⚙️ Stack technique

| Composant | Technologie |
|-----------|-------------|
| Framework | Django 6.0.3 |
| API | Django REST Framework 3.16.1 |
| Auth | JWT via SimpleJWT 5.5.1 |
| Base de données | PostgreSQL (psycopg 3.3.3) |
| Cache | Redis + django-redis 6.0.0 |
| Tâches asynchrones | Celery 5.6.2 |
| Documentation auto | drf-spectacular 0.29.0 (Swagger/ReDoc) |
| Admin UI | Django Jazzmin 3.0.3 |
| CORS | django-cors-headers 4.9.0 |
| Fichiers statiques | WhiteNoise 6.12.0 |

---

## 🔒 Permissions

| Permission | Description |
|-----------|-------------|
| `AllowAny` | Accessible sans authentification |
| `IsAuthenticated` | Requiert un token JWT valide |
| `AdminWriteOnlyPermission` | Lecture libre, écriture réservée aux admins (`is_staff=True`) |

---

## 📖 Documentation interactive (Swagger / ReDoc)

La documentation Swagger et ReDoc est disponible sur les URLs sécurisées définies dans les settings du projet. Contactez l'administrateur pour obtenir les URLs exactes.

---

## 📁 Structure du projet

```
Api/
├── Api/                    # Configuration principale Django
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── views.py            # health_check
├── user/                   # Authentification & profils
├── election_types/         # Types d'élection
├── elections/              # Élections
├── candidates/             # Candidats
├── candidate_results/      # Résultats (global, région, dept, diaspora)
├── political_parties/      # Partis politiques
├── regions/                # Régions du Cameroun
├── departments/            # Départements
├── voter_statistics/       # Statistiques globales électeurs
├── department_stats/       # Stats par département
├── region_stats/           # Stats par région
├── diaspora_stats/         # Stats diaspora
├── voting_office/          # Bureaux de vote
├── pickup_point/           # Points de retrait
├── calendrier_electoral/   # Calendrier électoral
└── utils/                  # Cache, signaux, tâches Celery
```
