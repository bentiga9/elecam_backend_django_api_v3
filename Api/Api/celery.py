"""
Configuration Celery pour ELECAM API
"""
import os
from celery import Celery

# Définir le module de settings par défaut pour Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Api.settings')

# Créer l'instance Celery
app = Celery('Api')

# Charger la configuration depuis les settings Django
# Tous les paramètres Celery doivent être préfixés par CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Découverte automatique des tâches dans les apps Django
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Tâche de debug pour tester Celery"""
    print(f'Request: {self.request!r}')
