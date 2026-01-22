from django.apps import AppConfig


class UtilsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'utils'
    verbose_name = 'Utilitaires'

    def ready(self):
        """
        Méthode appelée lorsque l'app est prête
        Enregistre automatiquement les signaux de cache
        """
        from .cache_signals import register_cache_signals
        register_cache_signals()