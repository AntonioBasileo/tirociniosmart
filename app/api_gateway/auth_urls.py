from django.urls import path
from security.view.auth_view import LoginView, RegisterTrainingUserView, RegisterAdminUserView

urlpatterns = [
    path('register-user', RegisterTrainingUserView.as_view(), name='register-user'),
    path('register-admin-user', RegisterAdminUserView.as_view(), name='register-admin-user'),
    path('login', LoginView.as_view(), name='login'),
]