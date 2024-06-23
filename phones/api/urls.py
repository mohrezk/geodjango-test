from django.urls import path
from .views import RequestPhoneVerificationTwilioView, VerifyPhoneNumberTwilioView,RequestPhoneVerificationSinchView
urlpatterns = [
    path('request-phone-verification-twilio/', RequestPhoneVerificationTwilioView.as_view(), name='request-phone-verification'),
    path('verify-phone-number-Twilio/', VerifyPhoneNumberTwilioView.as_view(), name='verify-phone-number'),

    path('request-phone-verification-sinch/', RequestPhoneVerificationSinchView.as_view(), name='request-phone-verification'),
    # path('verify-phone-number/', VerifyPhoneNumberSinchView.as_view(), name='verify-phone-number'),
]
