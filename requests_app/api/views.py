from rest_framework.generics import GenericAPIView
from requests_app.models import Request
from users.models import Customer, ServiceProvider
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import RequstSerializer
from rest_framework.response import Response
from rest_framework import status
from location.models import Location
from location.api.serializers import LocationSerializer, UserLocationSerializer

from users.api.serializers import UserSerializer


class CustomerRequestView(GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RequstSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = self.request.auth
        user = Token.objects.select_related("user").get(key=token).user
        customer = Customer.objects.select_related("user").get(user=user)
        user_location = Location.objects.select_related("user").get(user=user).location

        request_object = serializer.save(customer=customer)

        near_locations = Location.objects.filter(
            location__distance_lte=(user_location, 1000000000),
            user__is_customer=False,
        ).exclude(user=user)

        near_locations_serializer = UserLocationSerializer(near_locations, many=True)

        return Response(
            {"near_locations": near_locations_serializer.data},
            status=status.HTTP_201_CREATED,
        )
