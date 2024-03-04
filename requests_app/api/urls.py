from django.urls import path
from .views import CustomerRequestView


urlpatterns = [path("request-help/", CustomerRequestView.as_view())]
