"""
Tâches Celery pour ELECAM API
"""
from celery import shared_task
from django.core.cache import cache
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def clear_expired_cache(self):
    """
    Nettoie le cache expiré.
    Planifiable via Celery Beat.
    """
    try:
        # Django-redis gère automatiquement l'expiration,
        # mais on peut forcer un nettoyage si nécessaire
        cache.clear()
        logger.info("Cache nettoyé avec succès")
        return {"status": "success", "message": "Cache cleared"}
    except Exception as exc:
        logger.error(f"Erreur lors du nettoyage du cache: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True)
def send_election_notification(self, election_id, message):
    """
    Envoie une notification concernant une élection.
    """
    try:
        from elections.models import Election
        
        election = Election.objects.get(id=election_id)
        logger.info(f"Notification pour {election.title}: {message}")
        
        # Ici, on pourrait envoyer un email, une notification push, etc.
        return {
            "status": "success",
            "election": election.title,
            "message": message
        }
    except Exception as exc:
        logger.error(f"Erreur notification élection {election_id}: {exc}")
        return {"status": "error", "message": str(exc)}


@shared_task(bind=True)
def calculate_election_statistics(self, election_id):
    """
    Calcule et met à jour les statistiques d'une élection.
    """
    try:
        from elections.models import Election
        from candidate_results.models import CandidateGlobalResult
        from voter_statistics.models import VoterStatistics
        from department_stats.models import DepartmentStat
        from django.db.models import Sum
        
        election = Election.objects.get(id=election_id)
        
        # Calculer les totaux depuis les stats départementales
        dept_stats = DepartmentStat.objects.filter(election=election).aggregate(
            total_inscrits=Sum('inscrits'),
            total_votants=Sum('votants'),
            total_nuls=Sum('bulletins_nuls'),
            total_exprimes=Sum('suffrages_exprimes')
        )
        
        # Mettre à jour ou créer les statistiques globales
        stats, created = VoterStatistics.objects.update_or_create(
            election=election,
            defaults={
                'total_inscrits': dept_stats['total_inscrits'] or 0,
                'total_votants': dept_stats['total_votants'] or 0,
                'total_bulletins_nuls': dept_stats['total_nuls'] or 0,
                'total_suffrages_exprimes': dept_stats['total_exprimes'] or 0,
            }
        )
        
        # Calculer le taux de participation
        if stats.total_inscrits > 0:
            stats.taux_participation = (stats.total_votants / stats.total_inscrits) * 100
            stats.taux_abstention = 100 - stats.taux_participation
            stats.save()
        
        logger.info(f"Statistiques calculées pour {election.title}")
        return {
            "status": "success",
            "election": election.title,
            "total_inscrits": stats.total_inscrits,
            "total_votants": stats.total_votants,
            "taux_participation": float(stats.taux_participation)
        }
        
    except Exception as exc:
        logger.error(f"Erreur calcul stats élection {election_id}: {exc}")
        return {"status": "error", "message": str(exc)}


@shared_task
def health_check_task():
    """
    Tâche de vérification de santé pour Celery.
    Utilisée pour tester que Celery fonctionne correctement.
    """
    return {
        "status": "healthy",
        "timestamp": timezone.now().isoformat(),
        "message": "Celery worker is running"
    }
