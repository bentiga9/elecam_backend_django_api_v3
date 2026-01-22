from rest_framework import permissions


class AdminWriteOnlyPermission(permissions.BasePermission):
    """
    Permission personnalisée qui autorise :
    - Les requêtes GET, HEAD, OPTIONS sans authentification (lecture seule)
    - Les requêtes POST, PUT, PATCH, DELETE uniquement pour les administrateurs
    """
        
    def has_permission(self, request, view):
        # Autoriser les méthodes de lecture pour tout le monde
        if request.method in permissions.SAFE_METHODS:
            return True
                    
        # Pour les méthodes d'écriture, vérifier si l'utilisateur est authentifié et admin
        return request.user and request.user.is_authenticated and request.user.is_staff