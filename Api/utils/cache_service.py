import json
import hashlib
from typing import Any, Optional, Dict, List
from django.core.cache import cache
from django.conf import settings
from django.db import models
from django.http import HttpRequest
from rest_framework.response import Response
from functools import wraps
import logging

logger = logging.getLogger(__name__)

class CacheService:
    """
    Service de cache Redis intelligent avec invalidation automatique
    Cache TTL: 10 minutes par défaut
    """

    DEFAULT_TIMEOUT = 600  # 10 minutes

    @staticmethod
    def generate_cache_key(prefix: str, **kwargs) -> str:
        """Génère une clé de cache unique basée sur les paramètres"""
        # Créer un hash des paramètres pour garantir l'unicité
        param_str = json.dumps(kwargs, sort_keys=True, default=str)
        param_hash = hashlib.md5(param_str.encode()).hexdigest()[:8]
        return f"{prefix}:{param_hash}"

    @staticmethod
    def get_model_cache_prefix(model_class) -> str:
        """Retourne le préfixe de cache pour un modèle"""
        return f"{model_class._meta.app_label}:{model_class._meta.model_name}"

    @staticmethod
    def get_list_cache_key(model_class, **filters) -> str:
        """Génère une clé pour les listes d'objets"""
        prefix = f"{CacheService.get_model_cache_prefix(model_class)}:list"
        return CacheService.generate_cache_key(prefix, **filters)

    @staticmethod
    def get_detail_cache_key(model_class, pk) -> str:
        """Génère une clé pour un objet spécifique"""
        prefix = f"{CacheService.get_model_cache_prefix(model_class)}:detail"
        return CacheService.generate_cache_key(prefix, pk=pk)

    @staticmethod
    def get_stats_cache_key(model_class, stats_type: str = "general") -> str:
        """Génère une clé pour les statistiques"""
        prefix = f"{CacheService.get_model_cache_prefix(model_class)}:stats"
        return CacheService.generate_cache_key(prefix, type=stats_type)

    @staticmethod
    def set_cache(key: str, value: Any, timeout: int = None) -> bool:
        """Met en cache une valeur"""
        timeout = timeout or CacheService.DEFAULT_TIMEOUT
        try:
            cache.set(key, value, timeout)
            print(f"💾 CACHE SET: Données mises en cache Redis (TTL: {timeout}s) - {key}")
            logger.info(f"Cache set: {key} (TTL: {timeout}s)")
            return True
        except Exception as e:
            print(f"❌ ERREUR MISE EN CACHE: {key} - {e}")
            logger.error(f"Erreur lors de la mise en cache {key}: {e}")
            return False

    @staticmethod
    def get_cache(key: str) -> Any:
        """Récupère une valeur du cache"""
        try:
            value = cache.get(key)
            if value is not None:
                print(f"🟢 CACHE HIT: Données lues depuis Redis - {key}")
                logger.info(f"Cache hit: {key}")
            else:
                print(f"🔴 CACHE MISS: Données seront lues depuis PostgreSQL - {key}")
                logger.info(f"Cache miss: {key}")
            return value
        except Exception as e:
            print(f"❌ ERREUR CACHE: {key} - {e}")
            logger.error(f"Erreur lors de la lecture du cache {key}: {e}")
            return None

    @staticmethod
    def delete_cache(key: str) -> bool:
        """Supprime une clé du cache"""
        try:
            cache.delete(key)
            logger.info(f"Cache deleted: {key}")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la suppression du cache {key}: {e}")
            return False

    @staticmethod
    def invalidate_model_cache(model_class) -> bool:
        """Invalide tout le cache d'un modèle"""
        try:
            prefix = CacheService.get_model_cache_prefix(model_class)
            # Utiliser delete_many avec un pattern
            cache.delete_many(cache.keys(f"{prefix}:*"))
            logger.info(f"Cache invalidé pour le modèle: {model_class.__name__}")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de l'invalidation du cache pour {model_class.__name__}: {e}")
            return False

    @staticmethod
    def get_request_cache_params(request: HttpRequest) -> Dict:
        """Extrait les paramètres de requête pour le cache"""
        params = {}
        if hasattr(request, 'query_params'):
            params.update(request.query_params.dict())
        elif hasattr(request, 'GET'):
            params.update(request.GET.dict())

        # Ajouter des informations sur l'utilisateur si authentifié
        if hasattr(request, 'user') and request.user.is_authenticated:
            params['user_id'] = request.user.id
            params['user_role'] = getattr(request.user, 'role', 'user')

        return params


def cache_view_response(timeout: int = None, vary_on_user: bool = True):
    """
    Décorateur pour mettre en cache les réponses des vues API

    Args:
        timeout: Durée du cache en secondes (par défaut 10 minutes)
        vary_on_user: Si True, le cache varie selon l'utilisateur
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Générer la clé de cache
            cache_params = CacheService.get_request_cache_params(request)
            cache_params.update(kwargs)

            # Identifier la vue
            view_name = f"{view_func.__module__}.{view_func.__name__}"
            cache_key = CacheService.generate_cache_key(view_name, **cache_params)

            # Si on ne veut pas varier selon l'utilisateur, enlever les infos user
            if not vary_on_user:
                cache_params.pop('user_id', None)
                cache_params.pop('user_role', None)
                cache_key = CacheService.generate_cache_key(view_name, **cache_params)

            # Vérifier le cache
            cached_response = CacheService.get_cache(cache_key)
            if cached_response is not None:
                return Response(cached_response)

            # Exécuter la vue
            response = view_func(request, *args, **kwargs)

            # Mettre en cache si la réponse est valide
            if hasattr(response, 'data') and response.status_code == 200:
                CacheService.set_cache(cache_key, response.data, timeout)

            return response
        return wrapper
    return decorator


def cache_queryset(model_class, timeout: int = None):
    """
    Décorateur pour mettre en cache les querysets
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Générer la clé de cache
            cache_key = CacheService.generate_cache_key(
                f"{model_class.__name__}.{func.__name__}",
                args=args,
                kwargs=kwargs
            )

            # Vérifier le cache
            cached_result = CacheService.get_cache(cache_key)
            if cached_result is not None:
                return cached_result

            # Exécuter la fonction
            result = func(*args, **kwargs)

            # Mettre en cache le résultat
            if result is not None:
                CacheService.set_cache(cache_key, result, timeout)

            return result
        return wrapper
    return decorator