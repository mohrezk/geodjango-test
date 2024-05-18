from .views import LocationView,NearbyServiceProvidersAndUsers
from django.urls import path


urlpatterns = [
    path("set-location/", LocationView.as_view()),
    # path("get-nearby/", NearbyUsers.as_view()),
    path("get-all-nearby/", NearbyServiceProvidersAndUsers.as_view()),
                
]
