from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import CustomerRegisterSerializer, ServiceProviderRegisterSerializer, UserSerializer,UpdatePhoneNumberSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework import status

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
            # 'user':user.pk,
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            # 'is_customer':user.is_customer
        })
    

class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()

        return Response(status=status.HTTP_200_OK)

class UpdatePhoneNumberView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = UpdatePhoneNumberSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Phone number updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
