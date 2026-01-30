from django.db import models
from django.contrib.auth.models import User as AppUser


class Company(models.Model):
    name = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()

class Training(models.Model):
    request_date = models.DateTimeField(auto_now_add=True)
    limit_acceptance_date = models.DateTimeField()
    date_start = models.DateField()
    date_end = models.DateField()
    accepted = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)

class TrainingRegister(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)
    limit_confirmation_date = models.DateTimeField()