from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.postgres.fields import ArrayField

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    
    skills = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    specialty = models.CharField(max_length=255, blank=True, null=True)
    slogan = models.CharField(max_length=255, blank=True, null=True)
