from django.db import models
from django.conf import settings
from django.utils import timezone
import datetime

class PhoneVerification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    verification_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + datetime.timedelta(minutes=10)

    
    def __str__(self):
        return f"Phone for {self.user.username} is {self.phone_number}"