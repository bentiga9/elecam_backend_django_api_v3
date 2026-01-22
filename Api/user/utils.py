# user/utils.py
from django.core.mail import send_mail
from django.conf import settings
import random
import string


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
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")
        return False
