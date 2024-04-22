from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import CustomerRegisterSerializer, ServiceProviderRegisterSerializer, UserSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import update_session_auth_hash
from .serializers import ChangePasswordSerializer

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





class ChangePasswordAPIView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        old_password = serializer.validated_data.get('old_password')
        new_password = serializer.validated_data.get('new_password')

        if not user.check_password(old_password):
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)

        return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
