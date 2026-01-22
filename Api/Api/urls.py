from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from .views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # === HEALTH CHECK ===
    path('api/health-check/', health_check, name='health-check'),
    
    # === AUTHENTIFICATION ===
    path('api/auth/', include('user.urls')),
    
    # === STRUCTURE ÉLECTORALE ===
    path('api/election-types/', include('election_types.urls')),
    path('api/elections/', include('elections.urls')),
    path('api/regions/', include('regions.urls')),
    path('api/departments/', include('departments.urls')),  # NEW
    
    # === ACTEURS ===
    path('api/political-parties/', include('political_parties.urls')),
    path('api/candidates/', include('candidates.urls')),
    
    # === RÉSULTATS & STATISTIQUES ===
    path('api/voter-statistics/', include('voter_statistics.urls')),
    path('api/department-stats/', include('department_stats.urls')),
    path('api/region-stats/', include('region_stats.urls')),
    path('api/diaspora-stats/', include('diaspora_stats.urls')),
    path('api/candidate-results/', include('candidate_results.urls')),
    
    # === INFRASTRUCTURE (pour le futur) ===
    path('api/pickup-points/', include('pickup_point.urls')),
    path('api/voting-offices/', include('voting_office.urls')),
    path('api/calendrier-electoral/', include('calendrier_electoral.urls')),
    
    # === DOCUMENTATION API ===
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/kdlgdjkjdkvbsdhkjfvzemfnùpnoisdnfdoifnzufbzeufibzefzefumbmzfnsd/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/lkdfnsdljfbuigiuzpfbsidfvdstuzefmbfzeyfgvvfefefDFBDSFHBSDHFYUFBBQSDQSD/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Configuration pour servir les fichiers statiques en mode DEBUG=False
# WhiteNoise s'occupe normalement de cela, mais on ajoute une sécurité
if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT,
        }),
    ]