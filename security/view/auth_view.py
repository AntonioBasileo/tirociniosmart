from django.contrib.contenttypes.models import ContentType
from django.db import transaction
import json
import os
import time

from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group, Permission
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView

from app.dto.trainingDTOs import AppUserToDTO
from security.utility.jwt_util import encode_jwt


class LoginView(APIView):

    @staticmethod
    def get(request):
        try:
            body = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"detail": "Invalid JSON"}, status=400)

        username = body.get("username")
        password = body.get("password")

        if not username or not password:
            return Response("username/password required", status=HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response("Invalid credentials", status=HTTP_401_UNAUTHORIZED)

        now = int(time.time())
        exp = now + int(os.getenv("JWT_EXPIRATION_TIME"))

        payload = {
            "issuer": os.getenv("JWT_ISSUER"),
            "username": str(user.pk),
            "start": now,
            "exp": exp,
        }

        # python
        with open(os.getenv("JWT_SECRET_KEY_FILE"), "r") as f:
            jwt_secret = f.read().strip()

        token = encode_jwt(payload, secret=os.getenv("JWT_SECRET_KEY"))

        return Response({"access_token": token, "token_type": "Bearer", "expires_in": exp - now}, status=status.HTTP_200_OK)

def _resolve_or_create_permissions(perms):
    resolved = []

    for p in perms or ():
        app_label, codename = p.split('.', 1)

        try:
            resolved.append(Permission.objects.get(codename=codename))
            continue
        except Permission.DoesNotExist:
            pass

        model_name = codename.lower()[:100]
        perm, _ = Permission.objects.get_or_create(
            codename=codename,
            content_type=ContentType.objects.get_or_create(app_label=app_label, model=model_name)[0],
            defaults={'name': codename}
        )

        resolved.append(perm)

    return resolved

def register_user(request, group_name: str, permissions: list[str]):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"detail": "username/password required"}, status=HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        try:
            user = User.objects.create_user(username=username, password=password)
            group, _ = Group.objects.get_or_create(name=group_name)
            group.permissions.set(_resolve_or_create_permissions(permissions))
            user.groups.add(group)
        except Exception as e:
            return Response({"detail": f"Errore durante la registrazione: {str(e)}"}, status=HTTP_400_BAD_REQUEST)

        return Response({"details": "User successfully created", "user": AppUserToDTO(user).data}, status.HTTP_200_OK)


class RegisterTrainingUserView(APIView):

    @staticmethod
    def post(request):
        return register_user(request, group_name='training_user',
                             permissions=['app.training_register_view',
                                          'app.company_view'])


class RegisterAdminUserView(APIView):

    @staticmethod
    def post(request):
        return register_user(request,
                             group_name='admin',
                             permissions=['app.admin_view']
                             )
