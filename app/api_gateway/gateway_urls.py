from django.urls import path, include

urlpatterns = [
    path('api/training-register/', include('app.api_gateway.training_register_urls')),
    path('auth/', include('app.api_gateway.auth_urls')),
    path('api/company/', include('app.api_gateway.company_urls')),
]