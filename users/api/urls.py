from django.urls import path
from .views import (
    CustomerRegisterView,
    ServiceProviderRegisterView,
    CustomAuthToken,
    LogoutView,
    UpdatePhoneNumberView
)

urlpatterns=[
    path('signup/customer/', CustomerRegisterView.as_view()),
    path('signup/service-provider/', ServiceProviderRegisterView.as_view()),
    path('login/',CustomAuthToken.as_view(), name='auth-token'),
    path('logout/', LogoutView.as_view(), name='logout-view'),
    path('update-phone/', UpdatePhoneNumberView.as_view(), name='update-phone'),

]
