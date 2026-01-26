# 📚 Documentation API ELECAM - Endpoints GET

> **Version**: 2.0  
> **Base URL**: `https://your-domain.com/api/`  
> **Documentation Swagger**: `/api/docs/`

---

## Table des matières

1. [Health Check](#1-health-check)
2. [Authentification & Utilisateurs](#2-authentification--utilisateurs)
3. [Types d'élections](#3-types-délections)
4. [Élections](#4-élections)
5. [Régions](#5-régions)
6. [Départements](#6-départements)
7. [Partis Politiques](#7-partis-politiques)
8. [Candidats](#8-candidats)
9. [Statistiques Électorales](#9-statistiques-électorales)
10. [Statistiques par Département](#10-statistiques-par-département)
11. [Statistiques par Région](#11-statistiques-par-région)
12. [Statistiques Diaspora](#12-statistiques-diaspora)
13. [Résultats des Candidats](#13-résultats-des-candidats)
14. [Points de Retrait](#14-points-de-retrait)
15. [Bureaux de Vote](#15-bureaux-de-vote)
16. [Calendrier Électoral](#16-calendrier-électoral)

---

## 1. Health Check

### Vérifier l'état de l'API

```
GET /api/health-check/
```

**Description**: Vérifie que l'API est opérationnelle.

**Authentification**: Non requise

**Réponse**:
```json
{
  "status": "ok"
}
```

---

## 2. Authentification & Utilisateurs

### Obtenir le profil utilisateur

```
GET /api/auth/profile/
```

**Description**: Récupère les informations du profil de l'utilisateur connecté.

**Authentification**: Requise (JWT)

**Réponse**:
```json
{
  "id": 1,
  "email": "user@example.com",
  "nom": "John Doe"
}
```

---

### Compter le nombre d'utilisateurs

```
GET /api/auth/count/
```

**Description**: Retourne le nombre total d'utilisateurs enregistrés.

**Authentification**: Non requise

**Réponse**:
```json
{
  "count": 42
}
```

---

## 3. Types d'élections

### Liste des types d'élections

```
GET /api/election-types/
```

**Description**: Retourne la liste de tous les types d'élections disponibles.

**Authentification**: Non requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `search` | string | Recherche par nom ou description |
| `ordering` | string | Tri par nom (`name`, `-name`) |

**Réponse**:
```json
[
  {
    "id": 1,
    "name": "Présidentielle",
    "description": "Élection du Président de la République"
  }
]
```

---

### Détail d'un type d'élection

```
GET /api/election-types/{id}/
```

**Description**: Retourne les détails d'un type d'élection spécifique.

**Authentification**: Non requise

**Paramètres URL**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `id` | int | ID du type d'élection |

---

## 4. Élections

### Liste des élections

```
GET /api/elections/elections/
```

**Description**: Retourne la liste de toutes les élections avec filtres, recherche et tri.

**Authentification**: Non requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `type` | int | Filtrer par type d'élection (ID) |
| `status` | string | Filtrer par statut (`pending`, `ongoing`, `completed`) |
| `date_filter` | string | Filtrer par date (`future`, `past`, `today`) |
| `active_only` | bool | Afficher uniquement les élections actives |
| `search` | string | Recherche par titre ou description |
| `ordering` | string | Tri (`date`, `-date`, `created_at`, `title`) |

**Réponse**:
```json
[
  {
    "id": 1,
    "title": "Élection Présidentielle 2025",
    "type": {
      "id": 1,
      "name": "Présidentielle"
    },
    "date": "2025-10-06",
    "status": "completed",
    "candidates_count": 10
  }
]
```

---

### Détail d'une élection

```
GET /api/elections/elections/{id}/
```

**Description**: Retourne les détails complets d'une élection avec ses candidats.

**Authentification**: Non requise

**Paramètres URL**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `id` | int | ID de l'élection |

---

### Statistiques des élections

```
GET /api/elections/elections/statistics/
```

**Description**: Retourne les statistiques globales sur les élections.

**Authentification**: Non requise

**Réponse**:
```json
{
  "total_elections": 5,
  "elections_by_status": {
    "pending": 1,
    "ongoing": 0,
    "completed": 4
  },
  "elections_by_type": {
    "Présidentielle": 2,
    "Législatives": 3
  },
  "upcoming_elections": 1
}
```

---

## 5. Régions

### Liste des régions

```
GET /api/regions/
```

**Description**: Retourne la liste des 10 régions du Cameroun et des 4 zones diaspora.

**Authentification**: Non requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `region_type` | string | Filtrer par type (`national`, `diaspora`) |
| `is_active` | bool | Filtrer par statut actif |
| `search` | string | Recherche par nom, code ou chef-lieu |
| `ordering` | string | Tri (`name`, `code`, `region_type`) |

**Réponse**:
```json
[
  {
    "id": 1,
    "name": "Centre",
    "code": "CE",
    "chef_lieu": "Yaoundé",
    "region_type": "national",
    "departments": [...]
  }
]
```

---

### Détail d'une région

```
GET /api/regions/{id}/
```

**Description**: Retourne les détails d'une région avec ses départements.

**Authentification**: Non requise

---

## 6. Départements

### Liste des départements

```
GET /api/departments/
```

**Description**: Retourne la liste des 58 départements du Cameroun.

**Authentification**: Requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `region` | int | Filtrer par région (ID) |
| `region__code` | string | Filtrer par code région |
| `search` | string | Recherche par nom, code ou chef-lieu |
| `ordering` | string | Tri (`name`, `region`, `created_at`) |

---

### Détail d'un département

```
GET /api/departments/{id}/
```

**Description**: Retourne les détails d'un département.

**Authentification**: Requise

---

### Départements par région

```
GET /api/departments/by_region/
```

**Description**: Retourne les départements groupés par région.

**Authentification**: Requise

**Réponse**:
```json
{
  "Centre": [
    {"id": 1, "name": "Mfoundi", "code": "MF"}
  ],
  "Littoral": [
    {"id": 2, "name": "Wouri", "code": "WR"}
  ]
}
```

---

## 7. Partis Politiques

### Liste des partis politiques

```
GET /api/political-parties/parties/
```

**Description**: Retourne la liste de tous les partis politiques.

**Authentification**: Non requise

---

### Détail d'un parti politique

```
GET /api/political-parties/parties/{id}/
```

**Description**: Retourne les détails d'un parti politique.

**Authentification**: Non requise

---

## 8. Candidats

### Liste des candidats

```
GET /api/candidates/candidates/
```

**Description**: Retourne la liste de tous les candidats avec leurs partis politiques.

**Authentification**: Non requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `election` | int | Filtrer par élection (ID) |
| `partie_politique` | int | Filtrer par parti politique (ID) |
| `is_active` | bool | Filtrer par statut actif |
| `search` | string | Recherche par nom |
| `ordering` | string | Tri (`name`, `ballot_number`, `created_at`) |

---

### Détail d'un candidat

```
GET /api/candidates/candidates/{id}/
```

**Description**: Retourne les détails complets d'un candidat.

**Authentification**: Non requise

---

## 9. Statistiques Électorales

### Liste des statistiques globales

```
GET /api/voter-statistics/
```

**Description**: Retourne les statistiques globales de participation pour chaque élection.

**Authentification**: Non requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `election` | int | Filtrer par élection (ID) |
| `election__type` | int | Filtrer par type d'élection |
| `search` | string | Recherche par titre d'élection |
| `summary` | bool | Retourner un résumé simplifié |
| `ordering` | string | Tri (`created_at`, `taux_participation`, `total_inscrits`) |

**Réponse**:
```json
[
  {
    "id": 1,
    "election": {...},
    "total_inscrits": 7000000,
    "total_votants": 5000000,
    "taux_participation": 71.43,
    "bulletins_nuls": 50000,
    "suffrages_exprimes": 4950000
  }
]
```

---

### Détail des statistiques

```
GET /api/voter-statistics/{id}/
```

**Description**: Retourne les statistiques détaillées d'une élection.

**Authentification**: Non requise

---

## 10. Statistiques par Département

### Liste des statistiques départementales

```
GET /api/department-stats/departments/
```

**Description**: Retourne les statistiques de participation par département.

**Authentification**: Requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `election` | int | Filtrer par élection (ID) |
| `department` | int | Filtrer par département (ID) |
| `department__region` | int | Filtrer par région (ID) |
| `search` | string | Recherche par nom de département ou titre d'élection |
| `ordering` | string | Tri (`inscrits`, `votants`, `taux_participation`, `department__name`) |

---

### Détail d'une statistique départementale

```
GET /api/department-stats/departments/{id}/
```

**Description**: Retourne les détails d'une statistique départementale.

**Authentification**: Requise

---

### Statistiques agrégées par région

```
GET /api/department-stats/departments/by_region/
```

**Description**: Retourne les statistiques agrégées par région pour une élection.

**Authentification**: Requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `election_id` | int | **Requis** - ID de l'élection |

**Réponse**:
```json
[
  {
    "region_name": "Centre",
    "region_code": "CE",
    "total_inscrits": 1500000,
    "total_votants": 1000000,
    "taux_participation_moyen": 66.67,
    "total_bulletins_nuls": 10000,
    "total_suffrages_exprimes": 990000,
    "nombre_departements": 10
  }
]
```

---

### Résumé global des statistiques

```
GET /api/department-stats/departments/summary/
```

**Description**: Retourne un résumé global pour une élection.

**Authentification**: Requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `election_id` | int | **Requis** - ID de l'élection |

**Réponse**:
```json
{
  "total_inscrits": 7000000,
  "total_votants": 5000000,
  "taux_participation_global": 71.43,
  "total_bulletins_nuls": 50000,
  "total_suffrages_exprimes": 4950000,
  "nombre_departements": 58
}
```

---

## 11. Statistiques par Région

### Liste des statistiques régionales

```
GET /api/region-stats/region-stats/
```

**Description**: Retourne les statistiques de participation par région.

**Authentification**: Requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `election` | int | Filtrer par élection (ID) |
| `region` | int | Filtrer par région (ID) |
| `region__region_type` | string | Filtrer par type de région (`national`, `diaspora`) |
| `search` | string | Recherche par nom de région ou titre d'élection |
| `ordering` | string | Tri (`inscrits`, `votants`, `taux_participation`, `region__name`) |

---

### Détail d'une statistique régionale

```
GET /api/region-stats/region-stats/{id}/
```

**Description**: Retourne les détails d'une statistique régionale.

**Authentification**: Requise

---

### Statistiques par type de région

```
GET /api/region-stats/region-stats/by_type/
```

**Description**: Retourne les statistiques filtrées par type de région.

**Authentification**: Requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `election_id` | int | **Requis** - ID de l'élection |
| `region_type` | string | Type de région (`national`, `diaspora`) |

---

### Résumé des statistiques régionales

```
GET /api/region-stats/region-stats/summary/
```

**Description**: Retourne un résumé global des statistiques régionales.

**Authentification**: Requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `election_id` | int | **Requis** - ID de l'élection |

**Réponse**:
```json
{
  "total_inscrits": 7000000,
  "total_votants": 5000000,
  "taux_participation_global": 71.43,
  "total_bulletins_nuls": 50000,
  "total_suffrages_exprimes": 4950000,
  "nombre_regions": 14,
  "inscrits_national": 6500000,
  "votants_national": 4700000,
  "nombre_regions_nationales": 10,
  "inscrits_diaspora": 500000,
  "votants_diaspora": 300000,
  "nombre_zones_diaspora": 4
}
```

---

## 12. Statistiques Diaspora

### Liste des statistiques diaspora

```
GET /api/diaspora-stats/diaspora-stats/
```

**Description**: Retourne les statistiques de participation de la diaspora.

**Authentification**: Non requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `election` | int | Filtrer par élection (ID) |
| `zone` | string | Filtrer par zone (`AFRIQUE`, `AMERIQUE`, `ASIE`, `EUROPE`) |
| `search` | string | Recherche par zone ou titre d'élection |
| `ordering` | string | Tri (`zone`, `inscrits`, `votants`, `taux_participation`) |

---

### Détail d'une statistique diaspora

```
GET /api/diaspora-stats/diaspora-stats/{id}/
```

**Description**: Retourne les détails d'une statistique diaspora.

**Authentification**: Non requise

---

### Statistiques par élection

```
GET /api/diaspora-stats/diaspora-stats/by-election/{election_id}/
```

**Description**: Retourne toutes les statistiques diaspora pour une élection.

**Authentification**: Non requise

**Paramètres URL**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `election_id` | int | ID de l'élection |

---

### Statistiques par zone

```
GET /api/diaspora-stats/diaspora-stats/by-zone/{zone}/
```

**Description**: Retourne toutes les statistiques pour une zone diaspora.

**Authentification**: Non requise

**Paramètres URL**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `zone` | string | Code de la zone (`AFRIQUE`, `AMERIQUE`, `ASIE`, `EUROPE`) |

---

### Statistiques agrégées diaspora

```
GET /api/diaspora-stats/diaspora-stats/aggregate/{election_id}/
```

**Description**: Retourne les statistiques agrégées de toute la diaspora pour une élection.

**Authentification**: Non requise

**Paramètres URL**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `election_id` | int | ID de l'élection |

**Réponse**:
```json
{
  "total_inscrits": 500000,
  "total_votants": 300000,
  "taux_participation_moyen": 60.0,
  "total_bulletins_nuls": 5000,
  "total_suffrages_exprimes": 295000,
  "nombre_zones": 4,
  "details_par_zone": [...]
}
```

---

## 13. Résultats des Candidats

### 13.1 Résultats Globaux

#### Liste des résultats globaux

```
GET /api/candidate-results/global/
```

**Description**: Retourne le classement final des candidats pour une élection.

**Authentification**: Requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `election` | int | Filtrer par élection (ID) |
| `is_winner` | bool | Filtrer les gagnants uniquement |
| `ordering` | string | Tri (`rang`, `pourcentage_national`, `total_suffrages`) |

---

#### Détail d'un résultat global

```
GET /api/candidate-results/global/{id}/
```

**Description**: Retourne le détail du résultat global d'un candidat.

**Authentification**: Requise

---

#### Podium (Top 3)

```
GET /api/candidate-results/global/podium/
```

**Description**: Retourne les 3 premiers candidats d'une élection.

**Authentification**: Requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `election_id` | int | **Requis** - ID de l'élection |

---

#### Gagnant de l'élection

```
GET /api/candidate-results/global/winner/
```

**Description**: Retourne le candidat élu d'une élection.

**Authentification**: Requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `election_id` | int | **Requis** - ID de l'élection |

---

### 13.2 Résultats Régionaux

#### Liste des résultats régionaux

```
GET /api/candidate-results/regional/
```

**Description**: Retourne les résultats des candidats par région.

**Authentification**: Requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `election` | int | Filtrer par élection (ID) |
| `candidate` | int | Filtrer par candidat (ID) |
| `region` | int | Filtrer par région (ID) |
| `ordering` | string | Tri (`pourcentage`, `suffrages`, `region__name`) |

---

#### Détail d'un résultat régional

```
GET /api/candidate-results/regional/{id}/
```

**Description**: Retourne le détail d'un résultat régional.

**Authentification**: Requise

---

#### Résultats d'un candidat par région

```
GET /api/candidate-results/regional/by_candidate/
```

**Description**: Retourne les résultats d'un candidat dans toutes les régions.

**Authentification**: Requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `candidate_id` | int | **Requis** - ID du candidat |
| `election_id` | int | **Requis** - ID de l'élection |

---

#### Tous les candidats d'une région

```
GET /api/candidate-results/regional/by_region/
```

**Description**: Retourne tous les candidats pour une région donnée.

**Authentification**: Requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `region_id` | int | **Requis** - ID de la région |
| `election_id` | int | **Requis** - ID de l'élection |

---

### 13.3 Résultats Départementaux

#### Liste des résultats départementaux

```
GET /api/candidate-results/departmental/
```

**Description**: Retourne les résultats des candidats par département.

**Authentification**: Requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `election` | int | Filtrer par élection (ID) |
| `candidate` | int | Filtrer par candidat (ID) |
| `department` | int | Filtrer par département (ID) |
| `department__region` | int | Filtrer par région (ID) |
| `ordering` | string | Tri (`pourcentage`, `suffrages`, `department__name`) |

---

#### Détail d'un résultat départemental

```
GET /api/candidate-results/departmental/{id}/
```

**Description**: Retourne le détail d'un résultat départemental.

**Authentification**: Requise

---

#### Résultats d'un candidat par département

```
GET /api/candidate-results/departmental/by_candidate/
```

**Description**: Retourne les résultats d'un candidat dans tous les départements.

**Authentification**: Requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `candidate_id` | int | **Requis** - ID du candidat |
| `election_id` | int | **Requis** - ID de l'élection |

---

### 13.4 Résultats Diaspora

#### Liste des résultats diaspora

```
GET /api/candidate-results/diaspora/
```

**Description**: Retourne les résultats agrégés des candidats pour la diaspora (4 zones).

**Authentification**: Non requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `election` | int | Filtrer par élection (ID) |
| `candidate` | int | Filtrer par candidat (ID) |
| `ordering` | string | Tri (`pourcentage_diaspora`, `total_suffrages_diaspora`) |
| `search` | string | Recherche par nom de candidat ou parti |

---

#### Détail d'un résultat diaspora

```
GET /api/candidate-results/diaspora/{id}/
```

**Description**: Retourne le détail du résultat diaspora d'un candidat.

**Authentification**: Non requise

---

#### Classement diaspora

```
GET /api/candidate-results/diaspora/ranking/
```

**Description**: Retourne le classement des candidats pour la diaspora.

**Authentification**: Non requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `election` | int | **Requis** - ID de l'élection |

---

#### Résultats par zone diaspora

```
GET /api/candidate-results/diaspora/by-zone/
```

**Description**: Retourne les résultats d'un candidat détaillés par zone diaspora.

**Authentification**: Non requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `candidate` | int | **Requis** - ID du candidat |
| `election` | int | **Requis** - ID de l'élection |

**Réponse**:
```json
{
  "id": 1,
  "candidate": {...},
  "election": {...},
  "pourcentage_diaspora": 45.5,
  "total_suffrages_diaspora": 150000,
  "zones": [
    {"name": "Diaspora Afrique", "code": "DA", "suffrages": 40000},
    {"name": "Diaspora Amérique", "code": "DAM", "suffrages": 35000},
    {"name": "Diaspora Asie", "code": "DAS", "suffrages": 25000},
    {"name": "Diaspora Europe", "code": "DE", "suffrages": 50000}
  ]
}
```

---

## 14. Points de Retrait

### Liste des points de retrait

```
GET /api/pickup-points/
```

**Description**: Retourne la liste de tous les points de retrait.

**Authentification**: Non requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `type` | string | Filtrer par type |
| `date_from` | date | Date de début |
| `date_to` | date | Date de fin |
| `search` | string | Recherche textuelle |

---

### Détail d'un point de retrait

```
GET /api/pickup-points/{id}/
```

**Description**: Retourne les détails d'un point de retrait.

**Authentification**: Non requise

---

### Points de retrait par localisation

```
GET /api/pickup-points/by_location/
```

**Description**: Retourne les points de retrait dans une zone géographique.

**Authentification**: Non requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `lat_min` | float | Latitude minimale |
| `lat_max` | float | Latitude maximale |
| `lng_min` | float | Longitude minimale |
| `lng_max` | float | Longitude maximale |

---

### Points de retrait récents

```
GET /api/pickup-points/recent/
```

**Description**: Retourne les points de retrait créés dans les dernières 24h.

**Authentification**: Non requise

---

### Types de points disponibles

```
GET /api/pickup-points/types/
```

**Description**: Retourne la liste des types de points disponibles.

**Authentification**: Non requise

**Réponse**:
```json
{
  "types": ["pickup_point", "voting_office"]
}
```

---

### Compter les points de retrait

```
GET /api/pickup-points/count_pickup_points/
```

**Description**: Retourne le nombre total de points de retrait.

**Authentification**: Non requise

**Réponse**:
```json
{
  "nombre": 150
}
```

---

### Compter les bureaux de vote

```
GET /api/pickup-points/count_voting_offices/
```

**Description**: Retourne le nombre total de bureaux de vote.

**Authentification**: Non requise

**Réponse**:
```json
{
  "nombre": 25000
}
```

---

### Liste simple des points (API alternative)

```
GET /api/pickup-points/simple/list/
```

**Description**: API simple pour obtenir la liste paginée des points de retrait.

**Authentification**: Non requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `page` | int | Numéro de page (défaut: 1) |
| `limit` | int | Nombre d'éléments par page (défaut: 20) |

---

## 15. Bureaux de Vote

### Liste des bureaux de vote

```
GET /api/voting-offices/
```

**Description**: Retourne la liste de tous les bureaux de vote.

**Authentification**: Non requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `is_active` | bool | Filtrer par statut actif |
| `date_from` | date | Date de début |
| `date_to` | date | Date de fin |
| `search` | string | Recherche textuelle |

---

### Détail d'un bureau de vote

```
GET /api/voting-offices/{id}/
```

**Description**: Retourne les détails d'un bureau de vote.

**Authentification**: Non requise

---

### Statistiques des bureaux de vote

```
GET /api/voting-offices/statistics/
```

**Description**: Retourne des statistiques sur les bureaux de vote.

**Authentification**: Non requise

**Réponse**:
```json
{
  "total_offices": 25000,
  "active_offices": 24500,
  "inactive_offices": 500,
  "recent_offices": 50,
  "activity_rate": 98.0
}
```

---

### Bureaux de vote actifs

```
GET /api/voting-offices/active/
```

**Description**: Retourne uniquement les bureaux de vote actifs.

**Authentification**: Non requise

---

### Bureaux de vote inactifs

```
GET /api/voting-offices/inactive/
```

**Description**: Retourne uniquement les bureaux de vote inactifs.

**Authentification**: Non requise

---

### Bureaux de vote récents

```
GET /api/voting-offices/recent/
```

**Description**: Retourne les bureaux de vote créés dans les dernières 24h.

**Authentification**: Non requise

---

### Bureaux de vote par localisation

```
GET /api/voting-offices/by_location/
```

**Description**: Retourne les bureaux de vote dans une zone géographique.

**Authentification**: Non requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `lat_min` | float | Latitude minimale |
| `lat_max` | float | Latitude maximale |
| `lng_min` | float | Longitude minimale |
| `lng_max` | float | Longitude maximale |

---

### Liste simple des bureaux (API alternative)

```
GET /api/voting-offices/simple/list/
```

**Description**: API simple pour obtenir la liste paginée des bureaux de vote.

**Authentification**: Non requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `page` | int | Numéro de page (défaut: 1) |
| `limit` | int | Nombre d'éléments par page (défaut: 20) |

---

## 16. Calendrier Électoral

### Liste du calendrier électoral

```
GET /api/calendrier-electoral/
```

**Description**: Retourne la liste de toutes les élections du calendrier.

**Authentification**: Non requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `status` | string | Filtrer par statut (`planifie`, `en_cours`, `termine`, `reporte`, `annule`) |
| `type_election` | int | Filtrer par type d'élection (ID) |
| `date_from` | date | Date de début |
| `date_to` | date | Date de fin |
| `search` | string | Recherche textuelle |

---

### Détail d'une élection du calendrier

```
GET /api/calendrier-electoral/{id}/
```

**Description**: Retourne les détails d'une élection du calendrier.

**Authentification**: Non requise

---

### Statistiques du calendrier

```
GET /api/calendrier-electoral/statistics/
```

**Description**: Retourne des statistiques sur le calendrier électoral.

**Authentification**: Non requise

**Réponse**:
```json
{
  "total_elections": 10,
  "elections_planifiees": 2,
  "elections_en_cours": 1,
  "elections_terminees": 5,
  "elections_reportees": 1,
  "elections_annulees": 1,
  "elections_today": 0,
  "elections_upcoming": 3,
  "elections_past": 7
}
```

---

### Élections à venir

```
GET /api/calendrier-electoral/upcoming/
```

**Description**: Retourne les élections à venir.

**Authentification**: Non requise

---

### Élections du jour

```
GET /api/calendrier-electoral/today/
```

**Description**: Retourne les élections d'aujourd'hui.

**Authentification**: Non requise

---

### Élections par statut

```
GET /api/calendrier-electoral/by_status/
```

**Description**: Retourne les élections filtrées par statut.

**Authentification**: Non requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `status` | string | **Requis** - Statut (`planifie`, `en_cours`, `termine`, `reporte`, `annule`) |

---

### Élections récentes

```
GET /api/calendrier-electoral/recent/
```

**Description**: Retourne les élections créées dans les dernières 24h.

**Authentification**: Non requise

---

### Élections par type

```
GET /api/calendrier-electoral/by_type/
```

**Description**: Retourne les élections filtrées par type.

**Authentification**: Non requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `type_id` | int | **Requis** - ID du type d'élection |

---

### Liste simple du calendrier (API alternative)

```
GET /api/calendrier-electoral/simple/list/
```

**Description**: API simple pour obtenir la liste paginée du calendrier.

**Authentification**: Non requise

**Paramètres de requête**:
| Paramètre | Type | Description |
|-----------|------|-------------|
| `page` | int | Numéro de page (défaut: 1) |
| `limit` | int | Nombre d'éléments par page (défaut: 20) |

---

## 📝 Notes Générales

### Authentification

L'API utilise **JWT (JSON Web Token)** pour l'authentification.

Pour les endpoints nécessitant une authentification, inclure le header:
```
Authorization: Bearer <access_token>
```

### Codes de réponse HTTP

| Code | Signification |
|------|---------------|
| 200 | Succès |
| 201 | Ressource créée |
| 400 | Requête invalide |
| 401 | Non authentifié |
| 403 | Permission refusée |
| 404 | Ressource non trouvée |
| 500 | Erreur serveur |

### Pagination

La plupart des endpoints de liste supportent la pagination automatique via Django REST Framework.

### Filtres et Recherche

- **Filtres**: Utilisez les paramètres de requête pour filtrer les résultats
- **Recherche**: Utilisez le paramètre `search` pour une recherche textuelle
- **Tri**: Utilisez le paramètre `ordering` (préfixe `-` pour ordre décroissant)

---

*Documentation générée automatiquement - Dernière mise à jour: Janvier 2026*
