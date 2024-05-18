from location.models import Location
from rest_framework import generics

from .serializers import LocationSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from rest_framework.views import APIView
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.measure import Distance
from django.contrib.gis.geos import Point

class LocationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self, request):
        token = self.request.auth
        user = Token.objects.get(key=token).user

        location_data = request.data.get('location')

        location_instance = Location.objects.filter(user=user).first()
        
        if location_instance:
            serializer = LocationSerializer(location_instance, data={'location': location_data, 'timestamp': timezone.now()}, partial=True)

        else:
            serializer = LocationSerializer(data={'user': user.id, 'location': location_data, 'timestamp': timezone.now()})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class NearbyUsers(APIView):
#     def get(self, request, *args, **kwargs):
#         token = self.request.auth
#         user = Token.objects.get(key=token).user
#         radius = request.data.get("radius")

#         user_location = Location.objects.get(user=user).location

#         nearby_users_locations = Location.objects.filter(
#             location__distance_lte=(user_location, radius)
#         ).exclude(user=user)

#         nearby_users = [location.user.username for location in nearby_users_locations]

#         return Response({"nearby_users": nearby_users})

# لوكيشن 

class NearbyServiceProvidersAndUsers(APIView):
    def post(self, request, *args, **kwargs):
        token = self.request.auth
        user = Token.objects.get(key=token).user
        radius = request.data.get("radius", 5000)  # Default radius value if not provided
        service_type = request.data.get("service_type")
        
        # Extract current location from request body
        current_location_data = request.data.get("current_location")
        current_location = Point(current_location_data['longitude'], current_location_data['latitude'])

        if service_type:
            nearby_providers_locations = Location.objects.filter(
                location__distance_lte=(current_location, Distance(km=radius)),
                user__service_provider__services__contains=service_type
            ).exclude(user=user)
        else:
            nearby_providers_locations = Location.objects.filter(
                location__distance_lte=(current_location, Distance(km=radius))
            ).exclude(user=user)

        nearby_providers_info = [
            {"username": location.user.username, "service_type": location.user.service_provider.services, "location": (location.location.x, location.location.y)}
            for location in nearby_providers_locations
        ]

        nearby_users_locations = Location.objects.filter(
            location__distance_lte=(current_location, Distance(km=radius))
        ).exclude(user=user)

        nearby_users_info = [
            {"username": location.user.username, "location": (location.location.x, location.location.y)}
            for location in nearby_users_locations
        ]

        response_data = {
            "nearby_service_providers": nearby_providers_info,
            "nearby_users": nearby_users_info
        }

        return Response(response_data)
