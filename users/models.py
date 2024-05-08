from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)

    is_customer = models.BooleanField(default=False)
    is_service_provider = models.BooleanField(default=False)


    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)
    

    def __str__(self) -> str:
        return self.username


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="customer", on_delete=models.CASCADE)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)
    

    def __str__(self) -> str:
        return self.user.username
    

class ServiceProvider(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="service_provider", on_delete=models.CASCADE)
    services = models.CharField(max_length=255)
    description = models.CharField(max_length=255,blank=True, null=True)
    
    def __str__(self):
        return self.user.username