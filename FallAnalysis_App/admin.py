from django.contrib import admin
from .models import resident_detail, Resident_Health, Incident

@admin.register(resident_detail)
class ResidentDetailAdmin(admin.ModelAdmin):
    list_display = ('Resident_Name', 'Resident_ID', 'Resident_Age', 'Resident_Gender')
    search_fields = ('Resident_Name', 'Resident_ID')


@admin.register(Resident_Health)
class ResidentHealthAdmin(admin.ModelAdmin):
    list_display = ('resident', 'Doctor_Name', 'Doctor_Appointment')
    search_fields = ('resident__Resident_Name', 'Doctor_Name')


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('Resident', 'Incident_type', 'Incident_time', 'Incident_location')
    search_fields = ('Resident__Resident_Name', 'Incident_type')
