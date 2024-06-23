from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from ..models import PhoneVerification
import requests
from django.core.exceptions import ObjectDoesNotExist

from twilio.rest import Client
import random

class RequestPhoneVerificationTwilioView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

        verification_code = ''.join(random.choices('0123456789', k=4))

        PhoneVerification.objects.filter(user=user, phone_number=phone_number).delete()
        
        PhoneVerification.objects.create(user=user, phone_number=phone_number, verification_code=verification_code)

        # Initialize Twilio client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        try:
            # Send SMS
            message = client.messages.create(
                body=f"Your verification code is {verification_code}",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Verification code sent."}, status=status.HTTP_200_OK)


class VerifyPhoneNumberTwilioView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        phone_number = request.data.get('phone_number')
        verification_code = request.data.get('verification_code')

        if not phone_number or not verification_code:
            return Response({"error": "Phone number and verification code are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            verification_record = PhoneVerification.objects.get(user=user, phone_number=phone_number, verification_code=verification_code)
        except PhoneVerification.DoesNotExist:
            return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)

        if verification_record.is_expired():
            return Response({"error": "Verification code has expired."}, status=status.HTTP_400_BAD_REQUEST)

        user.phone_number = phone_number
        user.save()

        verification_record.delete()

        return Response({"message": "Phone number verified successfully."}, status=status.HTTP_200_OK)



#  Sinch


class RequestPhoneVerificationSinchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Remove any existing verification codes for this user and phone number
        PhoneVerification.objects.filter(user=user, phone_number=phone_number).delete()
        
        # Create a new verification record
        PhoneVerification.objects.create(user=user, phone_number=phone_number)

        # Sinch API URL and credentials
        sinch_url = "https://verification.api.sinch.com/verification/v1/verifications"
        headers = {"Content-Type": "application/json"}
        payload = {
            "identity": {
                "type": "number",
                "endpoint": phone_number
            },
            "method": "sms"
        }
        auth = (settings.SINCH_APP_KEY, settings.SINCH_APP_SECRET)

        try:
            # Send OTP via Sinch
            response = requests.post(sinch_url, json=payload, headers=headers, auth=auth)
            response.raise_for_status()
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Verification code sent."}, status=status.HTTP_200_OK)

class VerifyPhoneNumberSinchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        phone_number = request.data.get('phone_number')
        verification_code = request.data.get('verification_code')

        if not phone_number or not verification_code:
            return Response({"error": "Phone number and verification code are required."}, status=status.HTTP_400_BAD_REQUEST)

        sinch_url = f"https://verification.api.sinch.com/verification/v1/verifications/number/{phone_number}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "method": "sms",
            "sms": {
                "code": verification_code
            }
        }
        auth = (settings.SINCH_APP_KEY, settings.SINCH_APP_SECRET)

        try:
            # Verify OTP via Sinch
            response = requests.put(sinch_url, json=payload, headers=headers, auth=auth)
            response.raise_for_status()
            verification_status = response.json().get("status")
            if verification_status != "SUCCESSFUL":
                return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Update user's phone number
        user.phone_number = phone_number
        user.save()

        # Delete verification record
        PhoneVerification.objects.filter(user=user, phone_number=phone_number).delete()

        return Response({"message": "Phone number verified successfully."}, status=status.HTTP_200_OK)
