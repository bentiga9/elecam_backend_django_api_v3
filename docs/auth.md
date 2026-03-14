# 🔐 Authentification & Utilisateurs

> Base URL : `/api/auth/`

---

## 📋 Table des matières

- [Modèle Utilisateur](#modèle-utilisateur)
- [Inscription](#1-inscription)
- [Connexion](#2-connexion)
- [Déconnexion](#3-déconnexion)
- [Rafraîchir le token](#4-rafraîchir-le-token)
- [Profil](#5-profil-utilisateur)
- [Modifier le profil](#6-modifier-le-profil)
- [Changer le mot de passe](#7-changer-le-mot-de-passe)
- [Supprimer le compte](#8-supprimer-le-compte)
- [Réinitialisation du mot de passe](#9-réinitialisation-du-mot-de-passe)
- [Compter les utilisateurs](#10-compter-les-utilisateurs)

---

## 👤 Modèle Utilisateur

```json
{
  "id": 1,
  "email": "user@example.com",
  "nom": "Jean Dupont",
  "is_staff": false,
  "is_active": true,
  "date_joined": "2025-01-15T10:30:00Z"
}
```

| Champ | Type | Description |
|-------|------|-------------|
| `id` | integer | Identifiant unique |
| `email` | string | Email (identifiant de connexion) |
| `nom` | string | Nom complet de l'utilisateur |
| `is_staff` | boolean | `true` = administrateur |
| `is_active` | boolean | Compte actif |
| `date_joined` | datetime | Date d'inscription |

> ⚠️ L'authentification se fait par **email** (pas par username).

---

## 1. Inscription

**`POST /api/auth/register/`** — Public

### Corps de la requête

```json
{
  "email": "user@example.com",
  "nom": "Jean Dupont",
  "password": "MonMotDePasse123!",
  "password_confirm": "MonMotDePasse123!"
}
```

| Champ | Requis | Description |
|-------|--------|-------------|
| `email` | ✅ | Adresse email unique |
| `nom` | ✅ | Nom complet |
| `password` | ✅ | Mot de passe (min. 8 caractères) |
| `password_confirm` | ✅ | Confirmation du mot de passe |

### Réponse `201 Created`

```json
{
  "message": "Utilisateur créé avec succès",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "nom": "Jean Dupont"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  },
  "expires_in": "2 heures"
}
```

> 💡 Les admins reçoivent aussi un `refresh` token avec `expires_in: "24 heures"`.

### Erreurs possibles

| Code | Cause |
|------|-------|
| `400` | Email déjà utilisé, mots de passe non identiques, validation échouée |

---

## 2. Connexion

**`POST /api/auth/login/`** — Public

### Corps de la requête

```json
{
  "email": "user@example.com",
  "password": "MonMotDePasse123!"
}
```

### Réponse `200 OK`

```json
{
  "message": "Connexion réussie",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "nom": "Jean Dupont",
    "is_staff": false
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  },
  "expires_in": "2 heures"
}
```

### Erreurs possibles

| Code | Cause |
|------|-------|
| `400` | Données invalides |
| `401` | Email ou mot de passe incorrect |

---

## 3. Déconnexion

**`POST /api/auth/logout/`** — 🔒 Authentifié

Blackliste le refresh token pour invalider la session.

### En-tête requis

```http
Authorization: Bearer <access_token>
```

### Corps de la requête

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Réponse `200 OK`

```json
{
  "message": "Déconnexion réussie"
}
```

---

## 4. Rafraîchir le token

**`POST /api/auth/token/refresh/`** — Public

### Corps de la requête

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Réponse `200 OK`

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Erreurs possibles

| Code | Cause |
|------|-------|
| `401` | Refresh token invalide ou blacklisté |

---

## 5. Profil utilisateur

**`GET /api/auth/profile/`** — 🔒 Authentifié

### En-tête requis

```http
Authorization: Bearer <access_token>
```

### Réponse `200 OK`

```json
{
  "id": 1,
  "email": "user@example.com",
  "nom": "Jean Dupont",
  "is_staff": false,
  "is_active": true,
  "date_joined": "2025-01-15T10:30:00Z"
}
```

---

## 6. Modifier le profil

**`PUT /api/auth/profile/update/`** — 🔒 Authentifié  
**`PATCH /api/auth/profile/update/`** — 🔒 Authentifié (partiel)

### Corps de la requête (PATCH — partiel)

```json
{
  "nom": "Jean-Paul Dupont"
}
```

### Corps de la requête (PUT — complet)

```json
{
  "email": "nouveauemail@example.com",
  "nom": "Jean-Paul Dupont"
}
```

### Réponse `200 OK`

```json
{
  "id": 1,
  "email": "nouveauemail@example.com",
  "nom": "Jean-Paul Dupont",
  "is_staff": false
}
```

---

## 7. Changer le mot de passe

**`POST /api/auth/change-password/`** — 🔒 Authentifié

### Corps de la requête

```json
{
  "old_password": "AncienMotDePasse123!",
  "new_password": "NouveauMotDePasse456!",
  "new_password_confirm": "NouveauMotDePasse456!"
}
```

### Réponse `200 OK`

```json
{
  "message": "Mot de passe changé avec succès"
}
```

### Erreurs possibles

| Code | Cause |
|------|-------|
| `400` | Ancien mot de passe incorrect, nouveaux mots de passe non identiques |

---

## 8. Supprimer le compte

**`DELETE /api/auth/profile/delete/`** — 🔒 Authentifié

Supprime définitivement le compte de l'utilisateur connecté.

### Réponse `204 No Content`

```json
{
  "message": "Compte supprimé avec succès"
}
```

---

## 9. Réinitialisation du mot de passe

Processus en **3 étapes** :

### Étape 1 — Demander le code

**`POST /api/auth/password-reset/request/`** — Public

```json
{
  "email": "user@example.com"
}
```

**Réponse `200 OK`**
```json
{
  "message": "Un code de réinitialisation a été envoyé à votre adresse email"
}
```

> 📧 Un code à **4 chiffres** est envoyé par email. Il expire dans **15 minutes**.

---

### Étape 2 — Vérifier le code

**`POST /api/auth/password-reset/verify/`** — Public

```json
{
  "email": "user@example.com",
  "code": "1234"
}
```

**Réponse `200 OK`**
```json
{
  "message": "Code vérifié avec succès",
  "valid": true
}
```

**Erreurs**

| Code | Cause |
|------|-------|
| `400` | Code invalide ou expiré (> 15 min) |
| `404` | Email non trouvé |

---

### Étape 3 — Nouveau mot de passe

**`POST /api/auth/password-reset/confirm/`** — Public

```json
{
  "email": "user@example.com",
  "code": "1234",
  "new_password": "NouveauMotDePasse789!",
  "new_password_confirm": "NouveauMotDePasse789!"
}
```

**Réponse `200 OK`**
```json
{
  "message": "Mot de passe réinitialisé avec succès"
}
```

---

## 10. Compter les utilisateurs

**`GET /api/auth/count/`** — Public

### Réponse `200 OK`

```json
{
  "count": 42
}
```

---

## 💻 Exemples d'intégration

### Flutter / Dart

```dart
// Connexion
final response = await http.post(
  Uri.parse('$baseUrl/api/auth/login/'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'email': email,
    'password': password,
  }),
);

final data = jsonDecode(response.body);
final accessToken = data['tokens']['access'];
final refreshToken = data['tokens']['refresh'];

// Utiliser le token
final profileResponse = await http.get(
  Uri.parse('$baseUrl/api/auth/profile/'),
  headers: {
    'Authorization': 'Bearer $accessToken',
    'Content-Type': 'application/json',
  },
);
```

### Angular / TypeScript

```typescript
// login.service.ts
login(email: string, password: string): Observable<any> {
  return this.http.post(`${this.apiUrl}/auth/login/`, { email, password });
}

// Intercepteur HTTP pour ajouter le token
intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
  const token = localStorage.getItem('access_token');
  if (token) {
    req = req.clone({
      setHeaders: { Authorization: `Bearer ${token}` }
    });
  }
  return next.handle(req);
}
```
