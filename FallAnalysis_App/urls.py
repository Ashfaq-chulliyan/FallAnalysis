from django.urls import path
from . import views

urlpatterns = [
# Summary
    path('', views.summary, name="summary"),
    path('summary/', views.summary, name="summary"),
# Resident details
    path('resident_details/', views.resident_details, name="resident_details"),
# Data entry
    path('data_entry/', views.data_entry, name="data_entry"),
# Delete resident
    path('delete_resident/<int:resident_id>/', views.delete_resident, name="delete_resident"),
# Dashboard
    path('dashboard/', views.dashboard, name="dashboard"),
]
