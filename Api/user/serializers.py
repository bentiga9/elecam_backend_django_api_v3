# user/serializers.py
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import User
from .tokens import CustomRefreshToken


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer pour l'inscription d'un nouvel utilisateur"""
    password = serializers.CharField(
        write_only=True, 
        min_length=8,
        help_text="Mot de passe (minimum 8 caractères)"
    )
    password_confirm = serializers.CharField(
        write_only=True,
        help_text="Confirmation du mot de passe"
    )
    
    class Meta:
        model = User
        fields = ('email', 'nom', 'password', 'password_confirm')
        extra_kwargs = {
            'email': {
                'help_text': 'Adresse email unique',
                'error_messages': {
                    'unique': 'Cette adresse email est déjà utilisée.',
                    'invalid': 'Veuillez entrer une adresse email valide.',
                    'required': 'L\'adresse email est obligatoire.'
                }
            },
            'nom': {
                'help_text': 'Nom complet de l\'utilisateur',
                'error_messages': {
                    'required': 'Le nom est obligatoire.',
                    'max_length': 'Le nom ne peut pas dépasser 150 caractères.'
                }
            }
        }
    
    def validate_email(self, value):
        """Validation personnalisée pour l'email"""
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError("Cette adresse email est déjà utilisée.")
        return value.lower()
    
    def validate_password(self, value):
        """Validation personnalisée pour le mot de passe"""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value
    
    def validate(self, attrs):
        """Validation des données du formulaire"""
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({
                'password_confirm': 'Les mots de passe ne correspondent pas'
            })
        return attrs
    
    def create(self, validated_data):
        """Créer un nouvel utilisateur"""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer pour la connexion utilisateur avec JWT"""
    email = serializers.EmailField(
        help_text="Adresse email de l'utilisateur",
        error_messages={
            'invalid': 'Veuillez entrer une adresse email valide.',
            'required': 'L\'adresse email est obligatoire.'
        }
    )
    password = serializers.CharField(
        write_only=True,
        min_length=1,
        help_text="Mot de passe de l'utilisateur",
        error_messages={
            'required': 'Le mot de passe est obligatoire.',
            'min_length': 'Le mot de passe ne peut pas être vide.'
        }
    )
    
    def validate_email(self, value):
        """Normaliser l'email"""
        return value.lower()
    
    def validate(self, attrs):
        """Valider les identifiants et retourner l'utilisateur authentifié"""
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            # Vérifier si l'utilisateur existe
            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError('Identifiants invalides')
            
            # Authentifier l'utilisateur
            user = authenticate(username=email, password=password)
            
            if user and user.is_active:
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError('Identifiants invalides')
        else:
            raise serializers.ValidationError('Email et mot de passe requis')


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer pour les informations du profil utilisateur"""
    
    class Meta:
        model = User
        fields = ('id', 'email', 'nom', 'is_active', 'is_staff', 'date_joined')
        read_only_fields = ('id', 'email', 'date_joined', 'is_staff')
        extra_kwargs = {
            'nom': {
                'help_text': 'Nom complet de l\'utilisateur',
                'error_messages': {
                    'required': 'Le nom est obligatoire.',
                    'max_length': 'Le nom ne peut pas dépasser 150 caractères.'
                }
            }
        }
    
    def validate_nom(self, value):
        """Validation du nom"""
        if not value or not value.strip():
            raise serializers.ValidationError("Le nom ne peut pas être vide.")
        return value.strip()


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer pour le changement de mot de passe"""
    old_password = serializers.CharField(
        write_only=True,
        help_text="Ancien mot de passe",
        error_messages={
            'required': 'L\'ancien mot de passe est obligatoire.'
        }
    )
    new_password = serializers.CharField(
        write_only=True, 
        min_length=8,
        help_text="Nouveau mot de passe (minimum 8 caractères)",
        error_messages={
            'required': 'Le nouveau mot de passe est obligatoire.',
            'min_length': 'Le nouveau mot de passe doit contenir au moins 8 caractères.'
        }
    )
    
    def validate_new_password(self, value):
        """Validation du nouveau mot de passe"""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value


class TokenRefreshSerializer(serializers.Serializer):
    """Serializer pour le refresh des tokens JWT"""
    refresh = serializers.CharField(
        help_text="Token de rafraîchissement"
    )

    def validate(self, attrs):
        """Valider et rafraîchir le token"""
        refresh = attrs.get('refresh')
        try:
            refresh_token = CustomRefreshToken(refresh)
            data = {
                'access': str(refresh_token.access_token),
            }
            # Si on veut faire une rotation des refresh tokens
            if hasattr(refresh_token, 'rotate'):
                refresh_token.rotate()
                data['refresh'] = str(refresh_token)

            attrs['tokens'] = data
            return attrs
        except Exception as e:
            raise serializers.ValidationError('Token de rafraîchissement invalide')


class RequestPasswordResetSerializer(serializers.Serializer):
    """Serializer pour demander la réinitialisation du mot de passe"""
    email = serializers.EmailField(
        help_text="Adresse email du compte à réinitialiser",
        error_messages={
            'invalid': 'Veuillez entrer une adresse email valide.',
            'required': 'L\'adresse email est obligatoire.'
        }
    )

    def validate_email(self, value):
        """Normaliser l'email"""
        return value.lower()


class VerifyResetCodeSerializer(serializers.Serializer):
    """Serializer pour vérifier le code de réinitialisation"""
    email = serializers.EmailField(
        help_text="Adresse email du compte",
        error_messages={
            'invalid': 'Veuillez entrer une adresse email valide.',
            'required': 'L\'adresse email est obligatoire.'
        }
    )
    code = serializers.CharField(
        max_length=4,
        min_length=4,
        help_text="Code à 4 chiffres reçu par email",
        error_messages={
            'required': 'Le code de vérification est obligatoire.',
            'max_length': 'Le code doit contenir exactement 4 chiffres.',
            'min_length': 'Le code doit contenir exactement 4 chiffres.'
        }
    )

    def validate_email(self, value):
        """Normaliser l'email"""
        return value.lower()

    def validate_code(self, value):
        """Valider que le code contient uniquement des chiffres"""
        if not value.isdigit():
            raise serializers.ValidationError("Le code doit contenir uniquement des chiffres.")
        return value


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer pour réinitialiser le mot de passe"""
    email = serializers.EmailField(
        help_text="Adresse email du compte",
        error_messages={
            'invalid': 'Veuillez entrer une adresse email valide.',
            'required': 'L\'adresse email est obligatoire.'
        }
    )
    code = serializers.CharField(
        max_length=4,
        min_length=4,
        help_text="Code à 4 chiffres reçu par email",
        error_messages={
            'required': 'Le code de vérification est obligatoire.',
            'max_length': 'Le code doit contenir exactement 4 chiffres.',
            'min_length': 'Le code doit contenir exactement 4 chiffres.'
        }
    )
    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text="Nouveau mot de passe (minimum 8 caractères)",
        error_messages={
            'required': 'Le nouveau mot de passe est obligatoire.',
            'min_length': 'Le nouveau mot de passe doit contenir au moins 8 caractères.'
        }
    )

    def validate_email(self, value):
        """Normaliser l'email"""
        return value.lower()

    def validate_code(self, value):
        """Valider que le code contient uniquement des chiffres"""
        if not value.isdigit():
            raise serializers.ValidationError("Le code doit contenir uniquement des chiffres.")
        return value

    def validate_new_password(self, value):
        """Validation du nouveau mot de passe"""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value