# user/utils.py
import logging
import random
import string
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


def generate_reset_code():
    """
    Génère un code aléatoire à 4 chiffres pour la réinitialisation du mot de passe
    """
    return ''.join(random.choices(string.digits, k=4))


def send_reset_code_email(email, code, nom):
    """
    Envoie un email avec le code de réinitialisation du mot de passe

    Args:
        email (str): Adresse email du destinataire
        code (str): Code de réinitialisation à 4 chiffres
        nom (str): Nom de l'utilisateur

    Returns:
        bool: True si l'email a été envoyé avec succès, False sinon
    """
    subject = 'Code de réinitialisation de mot de passe - ELECAM'
    message = f"""
Bonjour {nom},

Vous avez demandé la réinitialisation de votre mot de passe.

Votre code de vérification est : {code}

Ce code est valide pendant 15 minutes.

Si vous n'avez pas demandé cette réinitialisation, veuillez ignorer cet email.

Cordialement,
L'équipe ELECAM
    """

    try:
        logger.info(f"[EMAIL] Envoi vers {email} depuis {settings.EMAIL_HOST_USER} via {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        logger.info(f"[EMAIL] ✅ Email envoyé avec succès à {email}")
        return True
    except Exception as e:
        logger.error(f"[EMAIL] ❌ Erreur envoi email à {email}: {type(e).__name__}: {str(e)}", exc_info=True)
        return False
