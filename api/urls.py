from django.urls import path
from .views import HomeAPI, MyTokenObtainPairView, StaffLoginAPI, PatientAPI

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', HomeAPI.as_view()),
    path('ishchi/', StaffLoginAPI.as_view()),
    path('bemor/', PatientAPI.as_view()),


    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]