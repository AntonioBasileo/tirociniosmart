from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from app.dto.trainingDTOs import CompanyToDTO
from app.model.training_models import Company
from app.permissions.permissions import CompanyPermissions


class CompanyView(APIView):
    permission_classes = [CompanyPermissions]

    @staticmethod
    def get(pk: int = None):
        if pk is not None:
            return Response(CompanyToDTO(Company.objects.get(pk=pk)).data, status=status.HTTP_200_OK)

        companies = Company.objects.all()
        return Response([CompanyToDTO(c).data for c in companies], status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        company = Company.objects.create(**request.data)
        return Response(CompanyToDTO(company).data, status=status.HTTP_200_OK)