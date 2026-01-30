from django.urls import path

from app.view.company_view import CompanyView

urlpatterns = [
    path('<int:pk>', CompanyView.as_view(), name='company-pk'),
    path('all', CompanyView.as_view(), name='company-all'),
]