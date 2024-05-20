from rest_framework import serializers

from users.models import User, Customer, ServiceProvider


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "is_customer"]


class CustomerRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self, **kwargs):
        username = self.validated_data.get("username")
        email = self.validated_data.get("email")
        first_name = self.validated_data.get("first_name")
        last_name = self.validated_data.get("last_name")
        password = self.validated_data.get("password")
        password2 = self.validated_data.get("password2")

        if None in (username, email, first_name, last_name, password, password2):
                raise serializers.ValidationError("All required fields must be provided.")

        if password != password2:
            raise serializers.ValidationError({"error": "password do not match"})
        
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        user.is_customer = True
        user.save()

        Customer.objects.create(user=user)

        return user


class ServiceProviderRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self, **kwargs):
        username = self.validated_data.get("username")
        email = self.validated_data.get("email")
        first_name = self.validated_data.get("first_name")
        last_name = self.validated_data.get("last_name")
        password = self.validated_data.get("password")
        password2 = self.validated_data.get("password2")

        if None in (username, email, first_name, last_name, password, password2):
                raise serializers.ValidationError("All required fields must be provided.")

        if password != password2:
            raise serializers.ValidationError({"error": "password do not match"})
        
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        user.is_service_provider = True
        user.save()

        ServiceProvider.objects.create(user=user)

        return user

from django.contrib.auth import get_user_model
User = get_user_model()

class UpdatePhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number']
