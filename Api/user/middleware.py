# user/middleware.py
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.http import JsonResponse
import json


class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware pour gérer l'authentification JWT avec des règles différentes 
    selon le type d'utilisateur
    """
    
    def process_request(self, request):
        """
        Traite la requête avant qu'elle n'atteigne la vue
        """
        # Exclure certaines URLs de la vérification JWT
        excluded_paths = [
            '/admin/',
            '/api/user/login/',
            '/api/user/register/',
            '/api/user/token/refresh/',
            '/api/user/count/',
        ]
        
        # Vérifier si le chemin est exclu
        if any(request.path.startswith(path) for path in excluded_paths):
            return None
        
        # Si c'est une requête vers l'admin, ne pas appliquer JWT
        if request.path.startswith('/admin/'):
            return None
        
        return None
    
    def process_response(self, request, response):
        """
        Traite la réponse avant qu'elle ne soit renvoyée au client
        """
        # Ajouter des headers personnalisés si nécessaire
        if hasattr(request, 'user') and request.user.is_authenticated:
            if hasattr(request.user, 'is_staff') and request.user.is_staff:
                response['X-User-Type'] = 'admin'
            else:
                response['X-User-Type'] = 'user'
                response['X-Token-Expires'] = '10-minutes'
        
        return response


class TokenExpirationMiddleware(MiddlewareMixin):
    """
    Middleware pour ajouter des informations sur l'expiration des tokens
    """
    
    def process_response(self, request, response):
        """
        Ajoute des informations sur l'expiration du token dans la réponse
        """
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Vérifier le type d'utilisateur et ajouter l'info d'expiration
            if hasattr(request.user, 'is_staff') and request.user.is_staff:
                response['X-Token-Lifetime'] = '24h'
            else:
                response['X-Token-Lifetime'] = '10min'
        
        return response