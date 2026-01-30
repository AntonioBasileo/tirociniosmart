from django.contrib.auth.decorators import permission_required
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.dto.trainingDTOs import CompanyToDTO
from app.model.training_models import Company


class CompanyView(APIView):

    @permission_required(['app.company_view', 'app.admin_view'], raise_exception=True)
    def get(self, pk: int):
        if pk is not None:
            return Response(CompanyToDTO(Company.objects.get(pk=pk)), status=status.HTTP_200_OK)

        return Response([CompanyToDTO(c) for c in Company.objects.all()], status=status.HTTP_200_OK)

    @permission_required('app.admin_view', raise_exception=True)
    def post(self, request):
        return Response(CompanyToDTO(Company.objects.create(**request.data)), status=status.HTTP_200_OK)
