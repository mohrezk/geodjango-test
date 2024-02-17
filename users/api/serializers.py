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
        user = User(
            username=self.validated_data["username"],
            email=self.validated_data["email"],
            first_name = self.validated_data["first_name"],
            last_name = self.validated_data["last_name"]
        )

        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"error": "password do not match"})
        
        user.set_password(password)
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
        user = User(
            username=self.validated_data["username"],
            email=self.validated_data["email"],
            first_name = self.validated_data["first_name"],
            last_name = self.validated_data["last_name"]
        )

        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"error": "password do not match"})
        
        user.set_password(password)
        user.is_service_provider = True
        user.save()

        ServiceProvider.objects.create(user=user)

        return user
