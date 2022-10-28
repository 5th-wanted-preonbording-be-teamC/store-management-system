from django.contrib.auth.models import AbstractUser

from django.db import models




class User(AbstractUser):
    address = models.CharField(max_length=100, blank=True, verbose_name="주소")
