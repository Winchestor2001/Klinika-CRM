from django.db import models
from django.contrib.auth.models import User


class Staff(models.Model):
    POSITION = (
        ('labarant', 'labarant'),
        ('reception', 'reception'),
        ('doctor', 'doctor'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    position = models.CharField(max_length=200, choices=POSITION)
    price = models.FloatField(default=0, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.full_name} - {self.position}"


class Service(models.Model):
    service_name = models.CharField(max_length=255)
    service_price = models.FloatField(default=0)

    def __str__(self) -> str:
        return str(self.service_name)


class Patient(models.Model):
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='doctor', null=True, blank=True)
    service = models.ManyToManyField(Service, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    pass_data = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    workplace = models.CharField(max_length=200)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='staff')
    inspaction = models.CharField(max_length=100)
    birthday = models.DateField(null=True)
    room_number = models.IntegerField(null=True, blank=True)
    total_sum = models.FloatField(default=0, null=True, blank=True)
    status = models.BooleanField(default=True)
    days = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.full_name)


class Analysis(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    assistent = models.ForeignKey(Staff, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.assistent)


class External(models.Model):
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE)
    analusis = models.ForeignKey(Analysis, on_delete=models.CASCADE)
    external = models.TextField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.doctor)


