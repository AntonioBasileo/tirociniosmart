from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.dto.trainingDTOs import TrainingRegisterDTO
from app.model.training_models import TrainingRegister


class TrainingRegisterView(APIView):

    @staticmethod
    @permission_required(['app.training_register_view', 'app.admin_view'], raise_exception=True)
    def get(pk: int):
        return Response(TrainingRegisterDTO(TrainingRegister.objects.get(pk=pk)), status=status.HTTP_200_OK)

    @staticmethod
    @permission_required(['app.training_register_view', 'app.admin_view'], raise_exception=True)
    def post(request):
        return Response(TrainingRegisterDTO(TrainingRegister.objects.create(**request.data)), status=status.HTTP_200_OK)


class TrainingRegisterDetailView(APIView):

    @staticmethod
    @permission_required(['app.training_register_detail_view', 'app.admin_view'], raise_exception=True)
    def put_or_patch(request, pk: int):
        TrainingRegister.objects.filter(pk=pk).update(**request.data)

        return Response("User successfully updated", status=status.HTTP_200_OK)

    @staticmethod
    @permission_required(['app.training_register_detail_view', 'app.admin_view'], raise_exception=True)
    def put(self, request, pk: int):
        return self.put_or_patch(request, pk)

    @staticmethod
    @permission_required(['app.training_register_detail_view', 'app.admin_view'], raise_exception=True)
    def patch(self, request, pk: int):
        return self.put_or_patch(request, pk)

    @staticmethod
    @permission_required(['app.training_register_detail_view', 'app.admin_view'], raise_exception=True)
    def delete(pk: int):
        TrainingRegister.objects.filter(pk=pk).delete()

        return Response("User successfully deleted", status=status.HTTP_200_OK)