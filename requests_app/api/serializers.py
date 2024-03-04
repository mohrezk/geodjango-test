from rest_framework import serializers
from requests_app.models import Request



class RequstSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=255)
    type = serializers.CharField(max_length=100)
    request_location = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Request.objects.create(**validated_data)


