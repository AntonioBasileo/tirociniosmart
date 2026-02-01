from django.utils.deprecation import MiddlewareMixin
from app.model.training_models import AppUser
from security.utility.jwt_util import decode_jwt, JWTError
import os


class JWTAuthenticationMiddleware(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        auth = request.META.get("HTTP_AUTHORIZATION", "")

        if not auth.startswith("Bearer "):
            return None

        token = auth[len("Bearer "):].strip()

        if not token:
            return None

        if request.path.startswith('/tirocinio-smart/'):
            setattr(request, '_dont_enforce_csrf_checks', True)

        secret_file = os.getenv("JWT_SECRET_KEY_FILE")
        if not secret_file:
            return None

        try:
            with open(secret_file, "r") as f:
                jwt_secret = f.read().strip()

            payload = decode_jwt(
                token,
                jwt_secret,
                os.environ.get("JWT_ISSUER", None),
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
        request._cached_user = user

        return None

