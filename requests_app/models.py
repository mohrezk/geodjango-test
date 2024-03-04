from django.contrib.gis.db import models
from users.models import Customer, ServiceProvider

# Create your models here.


class Request(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(
        ServiceProvider, on_delete=models.SET_NULL, null=True, blank=True
    )

    description = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default="Open")
    request_location = models.PointField()

    requested_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.description
