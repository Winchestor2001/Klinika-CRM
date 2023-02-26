from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .serializers import StaffSerializer, UserSerializer, PatientSerializer, ServiceSerializer
from .models import *
from django.contrib.auth import authenticate
import jwt
from backend import settings
from datetime import datetime, timedelta


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
                'get_doctors_GET': '/api/doctors/',
                'get_staff_POST_AND_GET': '/api/bemorlar/',
                'get_services_GET': '/api/xizmatlar/',
                'get_bemorlar_filter_GET': '/api/bemorlar_filter/',
                'check_pass_data_GET': '/api/check_pass_data/',
            }
        ]
        return Response({'status': 'OK', 'help_text': routes})


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
            user = get_object_or_404(User, username=username)
            serialize = UserSerializer(user)
            is_boss = True
        return Response({'status': 'OK', 'info': serialize.data, 'is_boss': is_boss})


class PatientAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        patient = Patient.objects.all()
        serialize = PatientSerializer(patient, many=True)
        return Response({'status': 'OK', 'info': serialize.data})

    def post(self, request):
        doctor = request.POST['doctor']
        service = request.POST['service']
        full_name = request.POST['full_name']
        pass_data = request.POST['pass_data']
        phone_number = request.POST['phone_number']
        address = request.POST['address']
        workplace = request.POST['workplace']
        inspaction = request.POST['inspaction']
        birthday = datetime.strptime(request.POST['birthday'], '%Y-%m-%d')
        room_number = request.POST['room_number'] if 'room_number' in request.POST else None
        staff = Staff.objects.get(user__username=decode_jwt_token(request))
        if doctor != 'no':
            doctor = get_object_or_404(Staff, id=int(doctor))
            patient = Patient.objects.create(
                doctor=doctor, full_name=full_name, pass_data=pass_data, phone_number=phone_number,
                address=address, workplace=workplace, inspaction=inspaction, room_number=room_number, staff=staff,
                birthday=birthday
            )
            if len(service) > 0:
                service = list(map(int, service.split(',')))
                total_sum = 0
                for s in service:
                    price = Service.objects.get(id=int(s))
                    total_sum += price.service_price
                    patient.service.add(s)
                patient.total_sum = total_sum
            patient.save()

        elif doctor == 'no' and len(service) == 0:
            Patient.objects.create(
                full_name=full_name, pass_data=pass_data, phone_number=phone_number,
                address=address, workplace=workplace, inspaction=inspaction, room_number=room_number, staff=staff,
                birthday=birthday
            )
        elif len(service) > 0:
            patient = Patient.objects.create(
                full_name=full_name, pass_data=pass_data, phone_number=phone_number, birthday=birthday,
                address=address, workplace=workplace, inspaction=inspaction, room_number=room_number, staff=staff, total_sum=0
            )
            service = list(map(int, service.split(',')))
            total_sum = 0
            for s in service:
                price = Service.objects.get(id=int(s))
                total_sum += price.service_price
                patient.service.add(s)
            patient.total_sum = total_sum
            patient.save()
        return Response({'status': 'OK'})


class ServiceAPI(APIView):
    def get(self, request):
        service = Service.objects.all()
        serialize = ServiceSerializer(service, many=True)
        return Response({'status': 'OK', 'services': serialize.data})


class AllStaffAPI(APIView):
    def get(self, request):
        doctors = Staff.objects.filter(position='doctor')
        serialize = StaffSerializer(doctors, many=True)
        return Response({'status': 'OK', 'doctors': serialize.data})


class PetientFilterAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.GET:
            inspaction = request.GET.get('rejim').capitalize()
            from_date = datetime.strptime(request.GET.get('from'), '%Y-%m-%d')
            to_date = datetime.strptime(request.GET.get('to'), '%Y-%m-%d') + timedelta(days=1)
            if from_date == to_date:
                patients = Patient.objects.filter(inspaction=inspaction).filter(created_date=from_date).order_by('-created_date')
            else:
                patients = Patient.objects.filter(inspaction=inspaction).filter(created_date__range=[from_date, to_date]).order_by('-created_date')
            serialize = PatientSerializer(patients, many=True)
            return Response({'status': 'OK', 'info': serialize.data})
        return Response({'status': 'ERROR'})



class CheckPAssDataAPI(APIView):
    def post(self, request):
        pass_data = request.data.get('pass_data')
        if Patient.objects.filter(pass_data=pass_data).exists():
            return Response({'status': 'true'})
        else:
            return Response({'status': 'false'})
