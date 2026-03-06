# user/views.py
import logging
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger(__name__)

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
    TokenRefreshSerializer,
    RequestPasswordResetSerializer,
    VerifyResetCodeSerializer,
    ResetPasswordSerializer
)
from .models import User
from .tokens import CustomRefreshToken
from .utils import generate_reset_code, send_reset_code_email
from django.utils import timezone
from datetime import timedelta


class RegisterView(APIView):
    """
    Vue d'inscription pour créer un nouvel utilisateur
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        summary="Inscription d'un nouvel utilisateur",
        description="Créer un nouveau compte utilisateur avec email et mot de passe",
        request=UserRegistrationSerializer,
        responses={
            201: {
                "description": "Utilisateur créé avec succès",
                "example": {
                    "message": "Utilisateur créé avec succès",
                    "user": {
                        "id": 1,
                        "email": "user@example.com",
                        "nom": "John Doe"
                    },
                    "tokens": {
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                    },
                    "expires_in": "10 minutes (utilisateur normal) / 24 heures (admin)"
                }
            },
            400: {"description": "Erreur de validation"},
        },
        tags=["Authentication"]
    )
    def post(self, request):
        logger.info(f"[REGISTER] Tentative d'inscription — data: {request.data}")
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"[REGISTER] ✅ Utilisateur créé: {user.email}")
            
            refresh = CustomRefreshToken.for_user(user)
            
            if isinstance(refresh, dict):
                expires_info = "2 heures"
                tokens_data = {"access": refresh['access']}
            else:
                expires_info = "24 heures"
                tokens_data = {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }
            
            return Response({
                "message": "Utilisateur créé avec succès",
                "user": UserProfileSerializer(user).data,
                "tokens": tokens_data,
                "expires_in": expires_info
            }, status=status.HTTP_201_CREATED)
        
        logger.warning(f"[REGISTER] ❌ Erreurs de validation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Vue de connexion pour authentifier un utilisateur
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        summary="Connexion utilisateur",
        description="Authentifier un utilisateur avec email et mot de passe",
        request=UserLoginSerializer,
        responses={
            200: {
                "description": "Connexion réussie",
                "example": {
                    "message": "Connexion réussie",
                    "user": {
                        "id": 1,
                        "email": "user@example.com",
                        "nom": "John Doe"
                    },
                    "tokens": {
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                    },
                    "expires_in": "10 minutes (utilisateur normal) / 24 heures (admin)"
                }
            },
            401: {"description": "Identifiants invalides"},
            400: {"description": "Données invalides"},
        },
        tags=["Authentication"]
    )
    def post(self, request):
        logger.info(f"[LOGIN] Tentative de connexion — email: {request.data.get('email', 'N/A')}")
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            logger.info(f"[LOGIN] ✅ Connexion réussie: {user.email} (is_staff={user.is_staff})")

            refresh = CustomRefreshToken.for_user(user)

            if isinstance(refresh, dict):
                expires_info = "2 heures"
                tokens_data = {"access": refresh['access']}
            else:
                expires_info = "24 heures"
                tokens_data = {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }

            return Response({
                "message": "Connexion réussie",
                "user": UserProfileSerializer(user).data,
                "tokens": tokens_data,
                "expires_in": expires_info
            }, status=status.HTTP_200_OK)

        logger.warning(f"[LOGIN] ❌ Échec connexion — email: {request.data.get('email', 'N/A')} — erreurs: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenRefreshView(APIView):
    """
    Vue pour rafraîchir les tokens JWT
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        summary="Rafraîchir le token d'accès",
        description="Obtenir un nouveau token d'accès en utilisant le refresh token",
        request=TokenRefreshSerializer,
        responses={
            200: {
                "description": "Token rafraîchi avec succès",
                "example": {
                    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                }
            },
            401: {"description": "Token de rafraîchissement invalide"},
        },
        tags=["Authentication"]
    )
    def post(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data['tokens'], status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


@extend_schema(
    summary="Profil utilisateur",
    description="Récupérer les informations du profil utilisateur connecté",
    responses={
        200: UserProfileSerializer,
        401: {"description": "Non authentifié"},
        403: {"description": "Permission refusée"},
    },
    tags=["Profile"]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """
    Vue pour récupérer le profil de l'utilisateur connecté
    """
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    summary="Déconnexion",
    description="Blacklister le refresh token pour déconnecter l'utilisateur",
    request={
        "type": "object",
        "properties": {
            "refresh": {"type": "string", "description": "Token de rafraîchissement à blacklister"}
        },
        "required": ["refresh"]
    },
    responses={
        200: {"description": "Déconnexion réussie"},
        400: {"description": "Token invalide"},
    },
    tags=["Authentication"]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Vue pour déconnecter l'utilisateur en blacklistant le refresh token
    """
    logger.info(f"[LOGOUT] Tentative — user: {request.user} — refresh présent: {'refresh' in request.data}")
    try:
        refresh_token = request.data.get("refresh")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f"[LOGOUT] ✅ Refresh token blacklisté pour: {request.user}")
        else:
            logger.warning(f"[LOGOUT] ⚠️ Pas de refresh token fourni pour: {request.user}")

        logout(request)
        return Response({"message": "Déconnexion réussie"}, status=status.HTTP_200_OK)
    except TokenError as e:
        logger.warning(f"[LOGOUT] ❌ Token invalide: {str(e)}")
        return Response({"error": "Token invalide"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"[LOGOUT] ❌ Erreur inattendue: {str(e)}", exc_info=True)
        logout(request)
        return Response({"message": "Déconnexion réussie"}, status=status.HTTP_200_OK)


@extend_schema(
    summary="Mettre à jour le profil",
    description="Modifier les informations du profil utilisateur",
    request=UserProfileSerializer,
    responses={
        200: UserProfileSerializer,
        400: {"description": "Erreur de validation"},
        401: {"description": "Non authentifié"},
    },
    tags=["Profile"]
)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile_view(request):
    """
    Vue pour mettre à jour le profil utilisateur
    """
    partial = request.method == 'PATCH'
    serializer = UserProfileSerializer(
        request.user, 
        data=request.data, 
        partial=partial
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Changer le mot de passe",
    description="Modifier le mot de passe de l'utilisateur connecté",
    request=ChangePasswordSerializer,
    responses={
        200: {
            "description": "Mot de passe changé avec succès",
            "example": {"message": "Mot de passe changé avec succès"}
        },
        400: {"description": "Erreur de validation ou ancien mot de passe incorrect"},
        401: {"description": "Non authentifié"},
    },
    tags=["Authentication"]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """
    Vue pour changer le mot de passe de l'utilisateur connecté
    """
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        
        # Vérifier l'ancien mot de passe
        if not user.check_password(old_password):
            return Response({
                "error": "Ancien mot de passe incorrect"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Changer le mot de passe
        user.set_password(new_password)
        user.save()
        
        return Response({
            "message": "Mot de passe changé avec succès"
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Supprimer son compte",
    description="Permet à un utilisateur de supprimer définitivement son propre compte",
    responses={
        204: {"description": "Compte supprimé avec succès"},
        401: {"description": "Non authentifié"},
    },
    tags=["Profile"]
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account_view(request):
    """
    Vue pour supprimer le compte de l'utilisateur connecté
    """
    user = request.user
    user.delete()
    return Response({
        "message": "Compte supprimé avec succès"
    }, status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    summary="Compter le nombre total d'utilisateurs",
    description="Retourne le nombre total d'utilisateurs enregistrés dans le système",
    responses={
        200: {
            "description": "Nombre total d'utilisateurs",
            "content": {
                "application/json": {
                    "example": {"count": 42}
                }
            }
        }
    },
    tags=["Utilisateurs"]
)
@api_view(['GET'])
@permission_classes([AllowAny])
def count_users_view(request):
    """
    Vue pour compter le nombre total d'utilisateurs
    """
    count = User.objects.count()
    return Response({"count": count}, status=status.HTTP_200_OK)


class RequestPasswordResetView(APIView):
    """
    Vue pour demander la réinitialisation du mot de passe
    Génère un code à 4 chiffres et l'envoie par email
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Demander la réinitialisation du mot de passe",
        description="Envoie un code à 4 chiffres par email pour réinitialiser le mot de passe",
        request=RequestPasswordResetSerializer,
        responses={
            200: {
                "description": "Code envoyé avec succès",
                "example": {
                    "message": "Un code de réinitialisation a été envoyé à votre adresse email"
                }
            },
            404: {"description": "Aucun compte associé à cet email"},
            500: {"description": "Erreur lors de l'envoi de l'email"},
        },
        tags=["Password Reset"]
    )
    def post(self, request):
        serializer = RequestPasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            # Vérifier si l'utilisateur existe
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({
                    "error": "Aucun compte n'est associé à cette adresse email"
                }, status=status.HTTP_404_NOT_FOUND)

            # Générer le code de réinitialisation
            reset_code = generate_reset_code()

            # Sauvegarder le code et la date de création
            user.reset_code = reset_code
            user.reset_code_created_at = timezone.now()
            user.save()

            # Envoyer l'email
            logger.info(f"[PASSWORD_RESET] Envoi du code {reset_code} à {email}")
            if send_reset_code_email(email, reset_code, user.nom):
                logger.info(f"[PASSWORD_RESET] ✅ Email envoyé à {email}")
                return Response({
                    "message": "Un code de réinitialisation a été envoyé à votre adresse email"
                }, status=status.HTTP_200_OK)
            else:
                logger.error(f"[PASSWORD_RESET] ❌ Échec envoi email à {email}")
                return Response({
                    "error": "Erreur lors de l'envoi de l'email. Veuillez réessayer plus tard."
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyResetCodeView(APIView):
    """
    Vue pour vérifier le code de réinitialisation
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Vérifier le code de réinitialisation",
        description="Vérifie si le code à 4 chiffres est valide et n'a pas expiré (15 minutes)",
        request=VerifyResetCodeSerializer,
        responses={
            200: {
                "description": "Code valide",
                "example": {
                    "message": "Code vérifié avec succès",
                    "valid": True
                }
            },
            400: {"description": "Code invalide ou expiré"},
            404: {"description": "Aucun compte associé à cet email"},
        },
        tags=["Password Reset"]
    )
    def post(self, request):
        serializer = VerifyResetCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']

            # Vérifier si l'utilisateur existe
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({
                    "error": "Aucun compte n'est associé à cette adresse email"
                }, status=status.HTTP_404_NOT_FOUND)

            # Vérifier si un code de réinitialisation existe
            if not user.reset_code or not user.reset_code_created_at:
                return Response({
                    "error": "Aucune demande de réinitialisation en cours"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Vérifier si le code a expiré (15 minutes)
            expiration_time = user.reset_code_created_at + timedelta(minutes=15)
            if timezone.now() > expiration_time:
                return Response({
                    "error": "Le code de réinitialisation a expiré"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Vérifier si le code correspond
            if user.reset_code != code:
                return Response({
                    "error": "Code de vérification invalide"
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "message": "Code vérifié avec succès",
                "valid": True
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    """
    Vue pour réinitialiser le mot de passe avec le code vérifié
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Réinitialiser le mot de passe",
        description="Réinitialise le mot de passe après vérification du code",
        request=ResetPasswordSerializer,
        responses={
            200: {
                "description": "Mot de passe réinitialisé avec succès",
                "example": {
                    "message": "Mot de passe réinitialisé avec succès"
                }
            },
            400: {"description": "Code invalide ou expiré"},
            404: {"description": "Aucun compte associé à cet email"},
        },
        tags=["Password Reset"]
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            new_password = serializer.validated_data['new_password']

            # Vérifier si l'utilisateur existe
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({
                    "error": "Aucun compte n'est associé à cette adresse email"
                }, status=status.HTTP_404_NOT_FOUND)

            # Vérifier si un code de réinitialisation existe
            if not user.reset_code or not user.reset_code_created_at:
                return Response({
                    "error": "Aucune demande de réinitialisation en cours"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Vérifier si le code a expiré (15 minutes)
            expiration_time = user.reset_code_created_at + timedelta(minutes=15)
            if timezone.now() > expiration_time:
                # Supprimer le code expiré
                user.reset_code = None
                user.reset_code_created_at = None
                user.save()
                return Response({
                    "error": "Le code de réinitialisation a expiré"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Vérifier si le code correspond
            if user.reset_code != code:
                return Response({
                    "error": "Code de vérification invalide"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Réinitialiser le mot de passe
            user.set_password(new_password)
            user.reset_code = None
            user.reset_code_created_at = None
            user.save()

            return Response({
                "message": "Mot de passe réinitialisé avec succès"
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)