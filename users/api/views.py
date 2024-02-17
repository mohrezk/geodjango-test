from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import CustomerRegisterSerializer, ServiceProviderRegisterSerializer, UserSerializer


class CustomerRegisterView(generics.GenericAPIView):
    serializer_class = CustomerRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message": "account created successfully"
        }, status=status.HTTP_201_CREATED)
    

class ServiceProviderRegisterView(generics.GenericAPIView):
    serializer_class = ServiceProviderRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            "token":Token.objects.get(user=user).key,
            "message":"account created successfully"
        }, status=status.HTTP_201_CREATED)
    


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token':token.key,
            'user_id':user.pk,
            'is_customer':user.is_customer
        })
    

class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()

        return Response(status=status.HTTP_200_OK)
