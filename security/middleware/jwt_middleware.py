from django.utils.deprecation import MiddlewareMixin

from app.model.training_models import AppUser
from security.utility.jwt_util import decode_jwt, JWTError
import os


class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    Se trova Authorization: Bearer <token>, valida il JWT e imposta request.user
    (sovrascrivendo l'AnonymousUser eventualmente già settato da AuthenticationMiddleware).
    """

    @staticmethod
    def process_request(request):
        auth = request.META.get("Authorization", "")

        if not auth.startswith("Bearer "):
            return None

        token = auth[len("Bearer "):].strip()

        if not token:
            return None

        try:
            payload = decode_jwt(
                token,
                os.environ.get("JWT_SECRET", None),
                os.environ.get("JWT_ISSUER", None)
            )
        except JWTError:
            return None

        user_id = payload.get("username")
        if not user_id:
            return None

        try:
            user = AppUser.objects.get(pk=user_id)
        except AppUser.DoesNotExist:
            return None

        request.user = user
        return user