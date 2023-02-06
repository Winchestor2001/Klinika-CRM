from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .serializers import StaffSerializer
from .models import Staff
from django.contrib.auth import authenticate



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class HomeAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'status':'OK'})


class UsersAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        users = Staff.objects.all()
        serializer = StaffSerializer(users, many=True)
        return Response({'users':serializer.data})


class StaffLoginAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        username = request.POST['username']
        staff = Staff.objects.get(user__username=username)
        serialize = StaffSerializer(staff)
        return Response({'status': 'OK', 'info': serialize.data})


