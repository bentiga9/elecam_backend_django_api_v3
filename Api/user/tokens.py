# user/tokens.py
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

class CustomRefreshToken(RefreshToken):
    """Token JWT personnalisé avec expiration différente selon le type d'utilisateur"""
    
    @classmethod
    def for_user(cls, user):
        """
        Crée un token avec une durée d'expiration différente selon le type d'utilisateur
        """
        if user.is_staff or user.is_superuser:
            # ---- Admin / Staff ----
            token = super().for_user(user)
            # Access Token : 24h
            token.access_token.set_exp(lifetime=timedelta(hours=24))
            # Refresh Token : 1 jour
            token.set_exp(lifetime=timedelta(days=1))
            # Claims personnalisés
            token['is_admin'] = True
            token['user_id'] = user.id
            token['email'] = user.email
            token['nom'] = getattr(user, "nom", "")
            token['is_staff'] = user.is_staff
            return token
        else:
            # ---- Utilisateur normal ----
            token = super().for_user(user)
            # Access Token : 10 min
            token.access_token.set_exp(lifetime=timedelta(minutes=10))
            # Refresh Token : court (30 min par exemple)
            token.set_exp(lifetime=timedelta(minutes=30))
            # Claims personnalisés
            token['is_admin'] = False
            token['user_id'] = user.id
            token['email'] = user.email
            token['nom'] = getattr(user, "nom", "")
            token['is_staff'] = user.is_staff
            return token