from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.apps import apps
from .cache_service import CacheService
import logging

logger = logging.getLogger(__name__)

class CacheManagement:
    """
    Utilitaires pour gérer le cache Redis
    """

    @staticmethod
    def clear_all_cache():
        """Vide complètement le cache Redis"""
        try:
            cache.clear()
            logger.info("Cache Redis complètement vidé")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la suppression du cache: {e}")
            return False

    @staticmethod
    def clear_app_cache(app_name):
        """Vide le cache d'une application spécifique"""
        try:
            app_config = apps.get_app_config(app_name)
            for model in app_config.get_models():
                CacheService.invalidate_model_cache(model)
            logger.info(f"Cache vidé pour l'app: {app_name}")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la suppression du cache pour {app_name}: {e}")
            return False

    @staticmethod
    def get_cache_stats():
        """Retourne des statistiques sur l'utilisation du cache"""
        try:
            # Note: Ces statistiques dépendent de votre configuration Redis
            # Vous pourriez avoir besoin d'ajuster selon votre setup
            stats = {
                'cache_backend': cache.__class__.__name__,
                'cache_location': getattr(cache, '_cache', {}).get('_server', 'N/A')
            }
            return stats
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des stats: {e}")
            return {}

    @staticmethod
    def warm_cache_for_app(app_name):
        """
        Préchauffe le cache pour une application
        (exécute les requêtes principales pour les mettre en cache)
        """
        try:
            app_config = apps.get_app_config(app_name)
            for model in app_config.get_models():
                # Préchauffe avec une requête de base
                queryset = model.objects.all()[:50]  # Limiter à 50 objets
                list(queryset)  # Force l'évaluation

                logger.info(f"Cache préchauffé pour {model.__name__}")

            logger.info(f"Cache préchauffé pour l'app: {app_name}")
            return True
        except Exception as e:
            logger.error(f"Erreur lors du préchauffage du cache pour {app_name}: {e}")
            return False


# Commande de management Django pour gérer le cache
class Command(BaseCommand):
    help = 'Commandes de gestion du cache Redis'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str, help='Action à effectuer: clear, clear_app, stats, warm')
        parser.add_argument('--app', type=str, help='Nom de l\'application pour clear_app ou warm')

    def handle(self, *args, **options):
        action = options['action']
        app_name = options.get('app')

        if action == 'clear':
            if CacheManagement.clear_all_cache():
                self.stdout.write(self.style.SUCCESS('Cache complètement vidé'))
            else:
                self.stdout.write(self.style.ERROR('Erreur lors de la suppression du cache'))

        elif action == 'clear_app':
            if not app_name:
                self.stdout.write(self.style.ERROR('--app requis pour clear_app'))
                return

            if CacheManagement.clear_app_cache(app_name):
                self.stdout.write(self.style.SUCCESS(f'Cache vidé pour {app_name}'))
            else:
                self.stdout.write(self.style.ERROR(f'Erreur lors de la suppression du cache pour {app_name}'))

        elif action == 'stats':
            stats = CacheManagement.get_cache_stats()
            for key, value in stats.items():
                self.stdout.write(f'{key}: {value}')

        elif action == 'warm':
            if not app_name:
                self.stdout.write(self.style.ERROR('--app requis pour warm'))
                return

            if CacheManagement.warm_cache_for_app(app_name):
                self.stdout.write(self.style.SUCCESS(f'Cache préchauffé pour {app_name}'))
            else:
                self.stdout.write(self.style.ERROR(f'Erreur lors du préchauffage pour {app_name}'))

        else:
            self.stdout.write(self.style.ERROR('Action non reconnue: clear, clear_app, stats, warm'))