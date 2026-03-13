"""
Custom email backend pour contourner les problèmes SSL sur macOS
"""
import ssl
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend


class CustomEmailBackend(SMTPBackend):
    """
    Backend email personnalisé qui désactive la vérification SSL stricte
    pour éviter les erreurs de certificat sur macOS avec Python 3.14
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ssl_context = None
    
    @property
    def ssl_context(self):
        if self._ssl_context is None:
            self._ssl_context = ssl.create_default_context()
            # Désactiver la vérification du certificat (dev uniquement)
            self._ssl_context.check_hostname = False
            self._ssl_context.verify_mode = ssl.CERT_NONE
        return self._ssl_context
