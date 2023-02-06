from django.db import models
from django.contrib.auth.models import User


class Staff(models.Model):
    POSITION = (
        ('Labarant', 'Labarant'),
        ('Reseption', 'Reseption'),
        ('Doctor', 'Doctor'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    position = models.CharField(max_length=200, choices=POSITION)

    def __str__(self) -> str:
        return self.full_name


class Patient(models.Model):
    full_name = models.CharField(max_length=200)
    pass_data = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    workplace = models.CharField(max_length=200)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    inspaction = models.CharField(max_length=100)
    room_number = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.full_name


class Service(models.Model):
    service_name = models.CharField(max_length=255)
    service_price = models.FloatField(default=0)

    def __str__(self) -> str:
        return self.service_name


class PatientService(models.Model):
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.doctor


class Analysis(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    assistent = models.ForeignKey(Staff, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.assistent


class External(models.Model):
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE)
    analusis = models.ForeignKey(Analysis, on_delete=models.CASCADE)
    external = models.TextField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.doctor


