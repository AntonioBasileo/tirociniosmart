from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.dto.trainingDTOs import TrainingRegisterDTO
from app.model.training_models import TrainingRegister
from app.permissions.permissions import TrainingPermissions


class TrainingRegisterView(APIView):
    permission_classes = [TrainingPermissions]

    @staticmethod
    def get(pk: int):
        return Response(TrainingRegisterDTO(TrainingRegister.objects.get(pk=pk)), status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        return Response(TrainingRegisterDTO(TrainingRegister.objects.create(**request.data)), status=status.HTTP_200_OK)


class TrainingRegisterDetailView(APIView):
    permission_classes = [TrainingPermissions]

    @staticmethod
    def put_or_patch(request, pk: int):
        TrainingRegister.objects.filter(pk=pk).update(**request.data)

        return Response("User successfully updated", status=status.HTTP_200_OK)

    @staticmethod
    def put(self, request, pk: int):
        return self.put_or_patch(request, pk)

    @staticmethod
    def patch(self, request, pk: int):
        return self.put_or_patch(request, pk)

    @staticmethod
    def delete(pk: int):
        TrainingRegister.objects.filter(pk=pk).delete()

        return Response("User successfully deleted", status=status.HTTP_200_OK)