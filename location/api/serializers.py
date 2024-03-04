from rest_framework import serializers
from location.models import Location
from users.models import User, ServiceProvider


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "is_customer"]


class UserLocationSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Location
        fields = ["user", "location", "timestamp"]
