"""
Django settings for Api project.
"""

from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-we!ve_(&m=7&(j5gxl5j(agt07r6tb**3qbx6$9q==co@ga77c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False  # Pour les tests et développement

ALLOWED_HOSTS = ['192.168.0.115', '192.168.0.106', '127.0.0.1', 'localhost', 'ielecambackend.efg-afroportal.com']  # Ajout testserver pour Django tests


# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',  # CORS package
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',  # JWT Package
    'rest_framework_simplejwt.token_blacklist',  # Pour la blacklist des tokens
    'drf_spectacular',
    'django_filters',
    
    # Apps métier - Authentification
    'user',
    
    # Apps métier - Structure électorale
    'election_types',           # Types d'élections (Présidentielle, Législative, etc.)
    'elections',                # Élections
    'regions',                  # Régions du Cameroun + Diaspora
    'departments',              # NEW: 58 départements du Cameroun
    
    # Apps métier - Acteurs
    'political_parties',        # Partis politiques
    'candidates',               # Candidats
    
    # Apps métier - Résultats & Statistiques
    'voter_statistics',         # Statistiques globales par élection
    'department_stats',         # Statistiques par département
    'region_stats',             # Statistiques par région
    'diaspora_stats',           # Statistiques diaspora par zone
    'candidate_results',        # Résultats détaillés des candidats
    
    # Apps métier - Infrastructure (pour le futur)
    'pickup_point',             # Points de retrait des cartes
    'voting_office',            # Bureaux de vote
    'calendrier_electoral',     # Calendrier électoral
    
    # Apps utilitaires
    'utils',                    # Cache Redis et utilitaires
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise pour les fichiers statiques
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware (doit être en haut)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Api.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Formatage des dates
USE_L10N = True
DATE_FORMAT = 'd/m/Y'
DATE_INPUT_FORMATS = [
    '%d/%m/%Y',  # '31/12/2023'
    '%d/%m/%y',  # '31/12/23'
    '%Y-%m-%d',  # '2023-12-31' (format ISO, par défaut)
]

DATETIME_FORMAT = 'd/m/Y H:i:s'
DATETIME_INPUT_FORMATS = [
    '%d/%m/%Y %H:%M:%S',     # '31/12/2023 14:30:59'
    '%d/%m/%Y %H:%M',        # '31/12/2023 14:30'
    '%d/%m/%y %H:%M:%S',     # '31/12/23 14:30:59'
    '%d/%m/%y %H:%M',        # '31/12/23 14:30'
    '%Y-%m-%d %H:%M:%S',     # '2023-12-31 14:30:59' (format ISO, par défaut)
    '%Y-%m-%d %H:%M:%S.%f',  # '2023-12-31 14:30:59.000200'
    '%Y-%m-%d %H:%M',        # '2023-12-31 14:30'
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Configuration WhiteNoise pour les fichiers statiques
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redis Configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://localhost:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'elecam_cache',
        'TIMEOUT': 300,  # 5 minutes par défaut
    }
}

# Configuration de l'encodage UTF-8
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'

# S'assurer que tous les champs de texte utilisent UTF-8
import sys
if sys.version_info >= (3, 0):
    import locale
    try:
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'French_France.1252')
        except locale.Error:
            pass

# Custom User Model
AUTH_USER_MODEL = 'user.User'

# Django REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT en premier
        'rest_framework.authentication.TokenAuthentication',  # Garde les tokens DRF pour l'admin si nécessaire
        'rest_framework.authentication.SessionAuthentication',  # Pour l'admin Django
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

# Configuration JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),  # 10 minutes pour les users normaux
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=10),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Swagger/OpenAPI Configuration
SPECTACULAR_SETTINGS = {
    'TITLE': 'ELECAM API - Elections Cameroon',
    'DESCRIPTION': '''
## 🗳️ API de Gestion des Élections du Cameroun (ELECAM)

Cette API permet de gérer l'ensemble du processus électoral au Cameroun.

### 📋 Fonctionnalités Principales

#### 🔐 Authentification
- Authentification JWT (JSON Web Token)
- Gestion des utilisateurs et des rôles

#### 🗳️ Gestion des Élections
- **Types d'élections**: Présidentielle, Législative, Municipale, Sénatoriale
- **Élections**: Création, suivi et gestion des élections
- **Candidats**: Gestion des candidats et leurs partis politiques

#### 🗺️ Découpage Territorial
- **Régions**: 10 régions nationales + 4 zones diaspora
- **Départements**: 58 départements du Cameroun

#### 📊 Résultats & Statistiques
- **Statistiques globales**: Inscrits, votants, taux de participation
- **Résultats par région/département**: Détails des votes par zone
- **Classement des candidats**: Résultats finaux avec pourcentages

#### 🏛️ Infrastructure Électorale
- **Bureaux de vote**: Localisation GPS et capacité
- **Points de retrait**: Cartes électorales
- **Calendrier électoral**: Événements et dates clés

### 🔑 Authentification

Utilisez le endpoint `/api/auth/login/` pour obtenir un token JWT.
Incluez le token dans le header: `Authorization: Bearer <token>`

### 📝 Notes
- Toutes les dates sont au format ISO 8601
- Les pourcentages sont exprimés en décimal (ex: 53.66 pour 53,66%)
- Les coordonnées GPS utilisent le format décimal
    ''',
    'VERSION': '2.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX': '/api/',
    'DEFAULT_GENERATOR_CLASS': 'drf_spectacular.generators.SchemaGenerator',
    
    # Organisation des tags
    'TAGS': [
        {'name': 'Authentification', 'description': 'Endpoints d\'authentification JWT'},
        {'name': 'Types d\'élections', 'description': 'Gestion des types d\'élections'},
        {'name': 'Élections', 'description': 'Gestion des élections'},
        {'name': 'Régions', 'description': 'Régions du Cameroun et zones diaspora'},
        {'name': 'Départements', 'description': '58 départements du Cameroun'},
        {'name': 'Partis politiques', 'description': 'Gestion des partis politiques'},
        {'name': 'Candidats', 'description': 'Gestion des candidats'},
        {'name': 'Statistiques globales', 'description': 'Statistiques électorales globales'},
        {'name': 'Statistiques départementales', 'description': 'Statistiques par département'},
        {'name': 'Statistiques régionales', 'description': 'Statistiques par région'},
        {'name': 'Statistiques diaspora', 'description': 'Statistiques par zone diaspora'},
        {'name': 'Résultats des candidats', 'description': 'Résultats détaillés des candidats'},
        {'name': 'Bureaux de vote', 'description': 'Gestion des bureaux de vote'},
        {'name': 'Points de retrait', 'description': 'Points de retrait des cartes électorales'},
        {'name': 'Calendrier électoral', 'description': 'Événements du calendrier électoral'},
    ],
    
    # Configuration Swagger UI
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': False,
        'filter': True,
        'showExtensions': True,
        'showCommonExtensions': True,
        'docExpansion': 'list',
        'defaultModelsExpandDepth': 2,
        'defaultModelExpandDepth': 2,
    },
    
    # Configuration pour JWT dans Swagger
    'COMPONENTS': {
        'securitySchemes': {
            'Bearer': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
                'description': 'Entrez votre token JWT. Exemple: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."'
            }
        }
    },
    'SECURITY': [{'Bearer': []}],
    
    # Informations de contact
    'CONTACT': {
        'name': 'ELECAM Support',
        'email': 'support@elecam.cm',
    },
    
    # Licence
    'LICENSE': {
        'name': 'Propriétaire - ELECAM Cameroun',
    },
    
    # Serveurs
    'SERVERS': [
        {'url': 'http://localhost:8000', 'description': 'Serveur de développement'},
        {'url': 'https://ielecambackend.efg-afroportal.com', 'description': 'Serveur de production'},
    ],
    
    # Tri des opérations
    'SORT_OPERATIONS': True,
    'SORT_OPERATION_PARAMETERS': True,
    
    # Enum
    'ENUM_NAME_OVERRIDES': {
        'ElectionStatusEnum': 'elections.models.Election.STATUS_CHOICES',
        'RegionTypeEnum': 'regions.models.Region.REGION_TYPE_CHOICES',
    },
}

# Configuration CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://192.168.0.106:4200",
]

# Pour le développement, vous pouvez utiliser :
CORS_ALLOW_ALL_ORIGINS = True  # ATTENTION: À désactiver en production

# Headers autorisés
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Méthodes autorisées
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Permettre les credentials (cookies, auth headers)
CORS_ALLOW_CREDENTIALS = True

# Configuration Email
# Pour le développement/test, utilisez le backend console qui affiche les emails dans la console
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_HOST_USER = 'noreply@elecam.com'
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Configuration Gmail pour l'envoi réel d'emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ielecam237@gmail.com'
EMAIL_HOST_PASSWORD = 'tylx gwnr xose rllz'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ============================================================
# CELERY CONFIGURATION
# ============================================================
# Broker Redis (même instance que le cache)
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Sérialisation
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Timezone
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True

# Tâches
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes max par tâche

# Résultats
CELERY_RESULT_EXPIRES = 3600  # Résultats expirés après 1 heure

# Retry
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True

# Beat Schedule (tâches planifiées)
CELERY_BEAT_SCHEDULE = {
    # Exemple: Nettoyer le cache tous les jours à minuit
    # 'clear-expired-cache': {
    #     'task': 'utils.tasks.clear_expired_cache',
    #     'schedule': crontab(hour=0, minute=0),
    # },
}