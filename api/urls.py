from django.urls import path

from api.views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
    path('register', UserRegistration.as_view()),
    path('get-token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user-details', UserDetailsAPIView.as_view(), name='user-details'),
    path('referral-details', ReferredUsers.as_view(), name='user-details'),
    
]
