from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.apps import apps
from utils.cache_service import CacheService
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Commandes de gestion du cache Redis pour ELECAM'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str,
                          choices=['clear', 'clear_app', 'stats', 'warm'],
                          help='Action à effectuer: clear, clear_app, stats, warm')
        parser.add_argument('--app', type=str,
                          help='Nom de l\'application pour clear_app ou warm')

    def handle(self, *args, **options):
        action = options['action']
        app_name = options.get('app')

        if action == 'clear':
            self.clear_all_cache()

        elif action == 'clear_app':
            if not app_name:
                self.stdout.write(self.style.ERROR('--app requis pour clear_app'))
                return
            self.clear_app_cache(app_name)

        elif action == 'stats':
            self.show_cache_stats()

        elif action == 'warm':
            if not app_name:
                self.stdout.write(self.style.ERROR('--app requis pour warm'))
                return
            self.warm_cache_for_app(app_name)

    def clear_all_cache(self):
        """Vide complètement le cache Redis"""
        try:
            cache.clear()
            self.stdout.write(self.style.SUCCESS('✓ Cache Redis complètement vidé'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Erreur lors de la suppression du cache: {e}'))

    def clear_app_cache(self, app_name):
        """Vide le cache d'une application spécifique"""
        try:
            app_config = apps.get_app_config(app_name)
            for model in app_config.get_models():
                CacheService.invalidate_model_cache(model)
            self.stdout.write(self.style.SUCCESS(f'✓ Cache vidé pour l\'app: {app_name}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Erreur lors de la suppression du cache pour {app_name}: {e}'))

    def show_cache_stats(self):
        """Affiche des statistiques sur le cache"""
        try:
            stats = {
                'Backend': cache.__class__.__name__,
                'Location': getattr(cache, '_cache', {}).get('_server', 'Redis localhost:6379'),
                'Timeout par défaut': f'{CacheService.DEFAULT_TIMEOUT} secondes (10 minutes)'
            }

            self.stdout.write(self.style.SUCCESS('📊 Statistiques du cache:'))
            for key, value in stats.items():
                self.stdout.write(f'  {key}: {value}')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Erreur lors de la récupération des stats: {e}'))

    def warm_cache_for_app(self, app_name):
        """Préchauffe le cache pour une application"""
        try:
            app_config = apps.get_app_config(app_name)
            models_warmed = 0

            for model in app_config.get_models():
                # Préchauffe avec une requête de base
                try:
                    queryset = model.objects.all()[:50]  # Limiter à 50 objets
                    list(queryset)  # Force l'évaluation
                    models_warmed += 1
                    self.stdout.write(f'  ✓ {model.__name__}')
                except Exception as e:
                    self.stdout.write(f'  ✗ {model.__name__}: {e}')

            self.stdout.write(
                self.style.SUCCESS(f'🔥 Cache préchauffé pour {app_name} ({models_warmed} modèles)')
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Erreur lors du préchauffage pour {app_name}: {e}'))