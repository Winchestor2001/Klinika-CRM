from django.contrib import admin
from .models import Staff, Service


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'position']
    search_fields = ['full_name', 'position']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'service_price']
    search_fields = ['service_name', 'service_price']



