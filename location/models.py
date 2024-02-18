from django.contrib.gis.db import models
from django.conf import settings



class Location(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.PointField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Location of {self.user.username} at {self.timestamp}"