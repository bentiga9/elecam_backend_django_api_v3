# user/models.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Manager personnalisé pour le modèle User"""
        
    def create_user(self, email, nom, password=None, **extra_fields):
        """Créer et sauvegarder un utilisateur normal"""
        if not email:
            raise ValueError('L\'adresse email est obligatoire')
        if not nom:
            raise ValueError('Le nom est obligatoire')
                
        email = self.normalize_email(email)
        user = self.model(email=email, nom=nom, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, nom, password=None, **extra_fields):
        """Créer et sauvegarder un superutilisateur"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superuser doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superuser doit avoir is_superuser=True.')
        
        return self.create_user(email, nom, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Modèle User personnalisé utilisant l'email comme identifiant"""

    email = models.EmailField(
        unique=True,
        verbose_name='Email',
        help_text='Adresse email unique de l\'utilisateur'
    )
    nom = models.CharField(
        max_length=150,
        verbose_name='Nom',
        help_text='Nom complet de l\'utilisateur'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Actif',
        help_text='Désigne si cet utilisateur doit être considéré comme actif.'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Statut équipe',
        help_text='Désigne si l\'utilisateur peut se connecter à l\'admin.'
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date d\'inscription'
    )
    reset_code = models.CharField(
        max_length=4,
        null=True,
        blank=True,
        verbose_name='Code de réinitialisation',
        help_text='Code à 4 chiffres pour réinitialiser le mot de passe'
    )
    reset_code_created_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Date de création du code',
        help_text='Date et heure de création du code de réinitialisation'
    )
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom']
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.nom} ({self.email})"
        
    def get_full_name(self):
        """Retourne le nom complet de l'utilisateur"""
        return self.nom
        
    def get_short_name(self):
        """Retourne le nom court de l'utilisateur"""
        return self.nom

# Suppression du signal create_auth_token puisqu'on utilise JWT maintenant