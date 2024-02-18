from .views import LocationView, NearbyUsers
from django.urls import path


urlpatterns = [
    path("set-location/", LocationView.as_view()),
    path("get-nearby/", NearbyUsers.as_view()),
                
]
