from django.db import models


class GrantedAuthorities(models.Model):
    username = models.CharField(max_length=100)
    authority = models.CharField(max_length=100)