from django.urls import path
from app.view.training_register_view import TrainingRegisterView, TrainingRegisterDetailView

urlpatterns = [
    path('', TrainingRegisterView.as_view(), name='training-register'),
    path('<int:pk>', TrainingRegisterDetailView.as_view(), name='training-register-pk'),
]