# Résultats Diaspora des Candidats

## Vue d'ensemble

Cette fonctionnalité permet de gérer les résultats agrégés des candidats pour la diaspora camerounaise, qui est divisée en 4 zones géographiques :

1. **Diaspora Afrique** (code: DA)
2. **Diaspora Amérique** (code: DAM)
3. **Diaspora Asie** (code: DAS)
4. **Diaspora Europe** (code: DE)

## Modèle de données

### CandidateDiasporaResult

Le modèle `CandidateDiasporaResult` stocke les résultats agrégés d'un candidat pour la diaspora.

**Champs principaux:**
- `election` - Élection concernée
- `candidate` - Candidat concerné
- `total_suffrages_diaspora` - Somme des suffrages des 4 zones diaspora
- `pourcentage_diaspora` - Pourcentage par rapport aux suffrages exprimés de la diaspora
- `suffrages_afrique` - Suffrages obtenus en Diaspora Afrique
- `suffrages_amerique` - Suffrages obtenus en Diaspora Amérique
- `suffrages_asie` - Suffrages obtenus en Diaspora Asie
- `suffrages_europe` - Suffrages obtenus en Diaspora Europe

**Contraintes:**
- Un seul résultat diaspora par candidat et par élection
- Contrainte unique sur (election, candidate)

## API Endpoints

### Liste des résultats diaspora
```http
GET /api/candidate-results/diaspora/
```

**Paramètres de filtrage:**
- `election` - Filtrer par ID d'élection
- `candidate` - Filtrer par ID de candidat
- `ordering` - Trier les résultats (ex: `-pourcentage_diaspora`)
- `search` - Rechercher par nom de candidat ou parti

**Exemple de réponse:**
```json
[
  {
    "id": 1,
    "election": 1,
    "election_title": "Élection Présidentielle 2025",
    "candidate": 5,
    "candidate_name": "NOM DU CANDIDAT",
    "party_name": "Parti Politique",
    "party_abbreviation": "PP",
    "total_suffrages_diaspora": 12500,
    "pourcentage_diaspora": 15.75,
    "suffrages_afrique": 3000,
    "suffrages_amerique": 4500,
    "suffrages_asie": 2000,
    "suffrages_europe": 3000,
    "created_at": "2025-01-20T10:00:00Z",
    "updated_at": "2025-01-20T10:00:00Z"
  }
]
```

### Détail d'un résultat diaspora
```http
GET /api/candidate-results/diaspora/{id}/
```

### Classement diaspora
```http
GET /api/candidate-results/diaspora/ranking/?election={election_id}
```

Retourne le classement des candidats triés par pourcentage diaspora décroissant.

**Paramètres requis:**
- `election` - ID de l'élection (obligatoire)

### Résultats par zone diaspora
```http
GET /api/candidate-results/diaspora/by-zone/?candidate={candidate_id}&election={election_id}
```

Retourne les détails d'un candidat avec un tableau détaillé des zones.

**Paramètres requis:**
- `candidate` - ID du candidat (obligatoire)
- `election` - ID de l'élection (obligatoire)

**Exemple de réponse:**
```json
{
  "id": 1,
  "election": 1,
  "candidate": 5,
  "total_suffrages_diaspora": 12500,
  "pourcentage_diaspora": 15.75,
  "zones": [
    {
      "name": "Diaspora Afrique",
      "code": "DA",
      "suffrages": 3000
    },
    {
      "name": "Diaspora Amérique",
      "code": "DAM",
      "suffrages": 4500
    },
    {
      "name": "Diaspora Asie",
      "code": "DAS",
      "suffrages": 2000
    },
    {
      "name": "Diaspora Europe",
      "code": "DE",
      "suffrages": 3000
    }
  ]
}
```

### Créer un résultat diaspora
```http
POST /api/candidate-results/diaspora/
```

**Permissions:** Administrateur uniquement

**Corps de la requête:**
```json
{
  "election": 1,
  "candidate": 5,
  "total_suffrages_diaspora": 12500,
  "pourcentage_diaspora": 15.75,
  "suffrages_afrique": 3000,
  "suffrages_amerique": 4500,
  "suffrages_asie": 2000,
  "suffrages_europe": 3000
}
```

### Mettre à jour un résultat
```http
PUT /api/candidate-results/diaspora/{id}/
PATCH /api/candidate-results/diaspora/{id}/
```

**Permissions:** Administrateur uniquement

### Supprimer un résultat
```http
DELETE /api/candidate-results/diaspora/{id}/
```

**Permissions:** Administrateur uniquement

## Import automatique des données

### Commande de gestion

Une commande Django est disponible pour calculer automatiquement les résultats diaspora à partir des résultats régionaux existants :

```bash
python manage.py import_diaspora_results_2025
```

**Options:**
- `--election-id` - ID de l'élection (par défaut: dernière élection active)

**Fonctionnement:**
1. Récupère tous les résultats régionaux pour les zones diaspora
2. Agrège les suffrages par candidat
3. Calcule le pourcentage moyen
4. Crée ou met à jour les résultats diaspora

**Prérequis:**
- Les zones diaspora doivent exister dans le modèle `Region` avec `region_type='diaspora'`
- Les résultats régionaux doivent être importés pour ces zones

## Interface d'administration

Le modèle est enregistré dans l'interface d'administration Django avec :

**Affichage de la liste:**
- Candidat
- Élection
- Total suffrages diaspora
- Pourcentage diaspora
- Suffrages par zone (Afrique, Amérique, Asie, Europe)

**Filtres:**
- Par élection

**Recherche:**
- Par nom de candidat
- Par nom de parti politique

**Organisation des champs:**
- Informations générales
- Résultats agrégés
- Détails par zone diaspora
- Métadonnées (dates de création/mise à jour)

## Permissions

- **Lecture (GET):** Accessible à tous (pas d'authentification requise)
- **Écriture (POST, PUT, PATCH, DELETE):** Réservé aux administrateurs authentifiés

## Relations avec d'autres modèles

- **Election:** Chaque résultat diaspora est lié à une élection spécifique
- **Candidat:** Chaque résultat est lié à un candidat
- **Region:** Utilise les régions de type `diaspora` pour les zones géographiques

## Notes techniques

- Les résultats diaspora sont stockés séparément des résultats régionaux pour faciliter l'agrégation
- Le pourcentage est calculé par rapport aux suffrages exprimés totaux de la diaspora
- Les données sont horodatées pour le suivi des modifications
- La contrainte d'unicité garantit qu'un candidat n'a qu'un seul résultat diaspora par élection
