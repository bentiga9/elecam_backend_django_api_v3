from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.apps import apps
from .cache_service import CacheService
import logging

logger = logging.getLogger(__name__)

class CacheInvalidationSignals:
    """
    Gestionnaire des signaux pour invalidation automatique du cache
    """

    @staticmethod
    def register_all_models():
        """
        Enregistre automatiquement les signaux pour tous les modèles de l'application
        """
        # Liste des apps à surveiller (exclut les apps système Django)
        monitored_apps = [
            'election_types', 'elections', 'regions', 'departments',
            'voter_statistics', 'department_stats', 'candidate_results',
            'political_parties', 'candidates',
            'pickup_point', 'voting_office',
            'calendrier_electoral', 'user'
        ]

        for app_name in monitored_apps:
            try:
                app_config = apps.get_app_config(app_name)
                for model in app_config.get_models():
                    CacheInvalidationSignals.register_model_signals(model)
                logger.info(f"Signaux de cache enregistrés pour l'app: {app_name}")
            except Exception as e:
                logger.warning(f"Impossible d'enregistrer les signaux pour {app_name}: {e}")

    @staticmethod
    def register_model_signals(model_class):
        """
        Enregistre les signaux pour un modèle spécifique
        """
        # Signal après sauvegarde
        @receiver(post_save, sender=model_class)
        def invalidate_on_save(sender, instance, created, **kwargs):
            CacheInvalidationSignals.handle_model_change(sender, instance, 'save', created)

        # Signal après suppression
        @receiver(post_delete, sender=model_class)
        def invalidate_on_delete(sender, instance, **kwargs):
            CacheInvalidationSignals.handle_model_change(sender, instance, 'delete')

    @staticmethod
    def handle_model_change(model_class, instance, action, created=False):
        """
        Gère l'invalidation du cache lors des changements de modèle
        """
        try:
            model_name = model_class.__name__

            # Invalidation du cache du modèle concerné
            CacheService.invalidate_model_cache(model_class)

            # Invalidation des caches liés (relations)
            CacheInvalidationSignals.invalidate_related_caches(model_class, instance)

            # Log de l'action
            action_text = "créé" if created else "modifié" if action == 'save' else "supprimé"
            logger.info(f"{model_name} {action_text} - Cache invalidé pour {model_name}")

        except Exception as e:
            logger.error(f"Erreur lors de l'invalidation du cache pour {model_class.__name__}: {e}")

    @staticmethod
    def invalidate_related_caches(model_class, instance):
        """
        Invalide les caches des modèles liés
        """
        model_name = model_class.__name__

        # Mapping des relations entre modèles
        relations_map = {
            'Election': ['ElectionType', 'Candidat', 'VoterStatistics'],
            'ElectionType': ['Election'],
            'Candidat': ['Election', 'PoliticalParty'],
            'PoliticalParty': ['Candidat'],
            'Region': ['VoterStatistics', 'RegionalStats'],
            'VoterStatistics': ['Election', 'Region'],
            'User': ['Election', 'Candidat'],  # Si les users sont liés aux élections
        }

        if model_name in relations_map:
            for related_model_name in relations_map[model_name]:
                try:
                    # Trouver le modèle lié
                    for app_name in ['election_types', 'elections', 'regions', 'departments',
                                   'voter_statistics', 'department_stats', 'candidate_results',
                                   'political_parties', 'candidates',
                                   'pickup_point', 'voting_office',
                                   'calendrier_electoral', 'user']:
                        try:
                            app_config = apps.get_app_config(app_name)
                            for model in app_config.get_models():
                                if model.__name__ == related_model_name:
                                    CacheService.invalidate_model_cache(model)
                                    logger.info(f"Cache du modèle lié invalidé: {related_model_name}")
                                    break
                        except:
                            continue
                except Exception as e:
                    logger.warning(f"Impossible d'invalider le cache pour le modèle lié {related_model_name}: {e}")


# Enregistrement automatique au démarrage
def register_cache_signals():
    """
    Fonction à appeler pour enregistrer tous les signaux de cache
    """
    CacheInvalidationSignals.register_all_models()
    logger.info("Tous les signaux de cache ont été enregistrés")