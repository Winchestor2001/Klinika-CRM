from django.urls import path
from .views import HomeAPI, MyTokenObtainPairView, UsersAPI, StaffLoginAPI

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', HomeAPI.as_view()),
    path('ishchilar/', UsersAPI.as_view()),
    path('ishchi/', StaffLoginAPI.as_view()),


    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]