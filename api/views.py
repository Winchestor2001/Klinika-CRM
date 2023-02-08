from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .serializers import StaffSerializer, UserSerializer, PatientSerializer
from .models import *
from django.contrib.auth import authenticate
import jwt
from backend import settings

def decode_jwt_token(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if token:
        jwt_token = request.headers['Authorization'].split()[-1]
        return jwt.decode(jwt_token, settings.SECRET_KEY, 'HS256')['username']
    return None


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        staff = Staff.objects.filter(user=user)
        if staff.exists():
            token['position'] = staff[0].position
        token['username'] = user.username

        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class HomeAPI(APIView):
    def get(self, request):
        routes = [
            {
                'get_access_token_POST': '/api/token/',
                'refresh_access_token_POST': '/api/token_refresh/',
                'get_staff_POST': '/api/ishchi/',
                'get_staff_POST_AND_GET': '/api/bemor/',
            }
        ]
        return Response({'status':'OK', 'help_text': routes})


class StaffLoginAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        username = decode_jwt_token(request)
        staff = Staff.objects.filter(user__username=username)
        if staff.exists():
            staff = Staff.objects.get(user__username=username)
            serialize = StaffSerializer(staff)
            is_boss = False
        else:
            user = User.objects.get(username=username)
            serialize = UserSerializer(user)
            is_boss = True
        return Response({'status': 'OK', 'info': serialize.data, 'is_boss': is_boss})
        # return Response({'status': 'OK'})


class PatientAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        patient = Patient.objects.all()
        serialize = PatientSerializer(patient, many=True)
        return Response({'status': 'OK', 'info': serialize.data})

    def post(self, request):
        pass



