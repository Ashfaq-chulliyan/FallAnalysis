from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db.models.functions import TruncMonth, TruncDay, TruncWeek, TruncHour # Added TruncHour
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
import json

from .models import (
    resident_detail as ResidentModel,
    Resident_Health,
    Incident,
    INCIDENT_CHOICES,
    INCIDENT_LOCATION_CHOICES
)

# ---------- basic dicision tree  ----------
def local_risk_prediction(resident_obj):
    past_falls = Incident.objects.filter(Resident=resident_obj).count()
    if resident_obj.Resident_Age > 80 and past_falls >= 2:
        return "High Risk"
    elif resident_obj.Resident_Age > 70 or past_falls > 0:
        return "Medium Risk"
    return "Low Risk"


# ---------- DASHBOARD ----------
def dashboard(request):
    period = request.GET.get('period', 'month')
    now = timezone.now()
    if period == 'day':
        start_date = now - timedelta(days=1)
        trunc_func = TruncHour("Incident_time")
        date_format = "%H:%M"
    elif period == 'week':
        start_date = now - timedelta(weeks=1)
        trunc_func = TruncDay("Incident_time")
        date_format = "%a"
    elif period == 'year':
        start_date = now - timedelta(days=365)
        trunc_func = TruncMonth("Incident_time")
        date_format = "%b %Y"
    else:  
        start_date = now - timedelta(days=30)
        trunc_func = TruncDay("Incident_time")
        date_format = "%d %b"

#---------filter time based-------------
    filtered_incidents = Incident.objects.filter(Incident_time__gte=start_date)
    total_incidents = filtered_incidents.count()
    total_approved_falls = filtered_incidents.filter(Incident_type="FA").count()
    total_residents = ResidentModel.objects.count()  
#------line chart---------
    incidents_by_time = (
        filtered_incidents
        .annotate(time_label=trunc_func)
        .values("time_label")
        .annotate(count=Count("id"))
        .order_by("time_label")
    )
    line_labels = [x["time_label"].strftime(date_format) if x["time_label"] else "N/A" for x in incidents_by_time]
    line_counts = [x["count"] for x in incidents_by_time]
#--------bar chart---------
    incident_location_counts = (
        filtered_incidents
        .values("Incident_location")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    location_dict = dict(INCIDENT_LOCATION_CHOICES)
    bar_labels = [location_dict.get(x["Incident_location"], x["Incident_location"]) for x in incident_location_counts]
    bar_counts = [x["count"] for x in incident_location_counts]
#------Pie chart--------------
    incident_type_counts = (
        filtered_incidents
        .values("Incident_type")
        .annotate(count=Count("id"))
        .order_by("Incident_type")
    )
    incident_dict = dict(INCIDENT_CHOICES)
    pie2_labels = [incident_dict.get(x["Incident_type"], x["Incident_type"]) for x in incident_type_counts]
    pie2_counts = [x["count"] for x in incident_type_counts]
#------Recent Incident----------
    recent_incidents = filtered_incidents.select_related("Resident").order_by("-Incident_time")[:5]

    context = {
        "total_incidents": total_incidents,
        "total_approved_falls": total_approved_falls,
        "total_residents": total_residents,

        "line_labels": json.dumps(line_labels),
        "line_counts": json.dumps(line_counts),

        "bar_labels": json.dumps(bar_labels), 
        "bar_counts": json.dumps(bar_counts),

        "pie2_labels": json.dumps(pie2_labels),
        "pie2_counts": json.dumps(pie2_counts),

        "recent_incidents": recent_incidents,
        "period": period, 
    }

    return render(request, "dashboard.html", context)




# ---------- SUMMARY ----------
def summary(request):
    agg_type = request.GET.get("agg_type", "month")

    total_residents = ResidentModel.objects.count()
    total_falls = Incident.objects.count()
    recent_residents = Incident.objects.select_related("Resident").order_by("-Incident_time")[:5]
#-----day,week filter using aggregation method-----------
    if agg_type == "day":
        trunc_func = TruncDay("Incident_time")
        fmt = "%d %b"
    elif agg_type == "week":
        trunc_func = TruncWeek("Incident_time")
        fmt = "Wk %W"
    else:
        trunc_func = TruncMonth("Incident_time")
        fmt = "%b %Y"

    fall_stats = (
        Incident.objects
        .annotate(period=trunc_func)
        .values("period")
        .annotate(count=Count("id"))
        .order_by("period")
    )

    labels = [x["period"].strftime(fmt) if x["period"] else "N/A" for x in fall_stats]
    counts = [x["count"] for x in fall_stats]

#resident risk decision tree
    resident_risks = []
    for res in ResidentModel.objects.all():
        resident_risks.append({
            "name": res.Resident_Name,
            "age": res.Resident_Age,
            "risk": local_risk_prediction(res)
        })

    context = {
        "total_residents": total_residents,
        "total_falls": total_falls,
        "recent_residents": recent_residents,
        "risk_level": "Moderate" if total_falls > 0 else "Stable",
        "months": labels,
        "monthly_counts": counts,
        "agg_type": agg_type,
        "resident_risks": resident_risks,
    }

    return render(request, "summary.html", context)


# ---------- DATA ENTRY ----------
def data_entry(request):
    residents = ResidentModel.objects.all().order_by("-id")
    popup_message = ""

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        try:
            if form_type == "resident":
                ResidentModel.objects.create(
                    Resident_ID=int(request.POST.get("Resident_ID")),
                    Resident_Name=request.POST.get("Resident_Name"),
                    Resident_Age=int(request.POST.get("Resident_Age") or 0),
                    Resident_Gender=request.POST.get("Resident_Gender"),
                    Resident_DateOfBirth=request.POST.get("Resident_DateOfBirth") or None,
                    Resident_AdmissionDate=request.POST.get("Resident_AdmissionDate") or None,
                    Resident_Phone=request.POST.get("Resident_Phone"),
                    Resident_GuardianName=request.POST.get("Resident_GuardianName"),
                    Resident_GuardianPhone=request.POST.get("Resident_GuardianPhone"),
                )
                messages.success(request, "New resident added successfully!")
                return redirect("data_entry")
            elif form_type == "health":
                resident = get_object_or_404(ResidentModel, id=request.POST.get("Resident_ID"))
                Resident_Health.objects.create(
                    resident=resident,
                    Physical_condition=request.POST.get("Physical_condition"),
                    History=request.POST.get("History"),
                    Medication=request.POST.get("Medication"),
                    Doctor_Name=request.POST.get("Doctor_Name"),
                    Doctor_Appointment=request.POST.get("Doctor_Appointment") or None,
                    Doctor_Contact=request.POST.get("Doctor_Contact"),
                )
                messages.success(request, f"Health record saved for {resident.Resident_Name}")
                return redirect("data_entry")
            elif form_type == "incident":
                resident = get_object_or_404(ResidentModel, id=request.POST.get("Resident_ID"))
                latest_health = Resident_Health.objects.filter(resident=resident).last()
                Incident.objects.create(
                    Resident=resident,
                    Health_Record=latest_health,
                    Incident_type=request.POST.get("Incident_type"),
                    Incident_time=request.POST.get("Incident_time") or None,
                    Incident_location=request.POST.get("Incident_location"),
                    Injury_level=request.POST.get("Injury_level"),
                )
                messages.success(request, f"Incident logged for {resident.Resident_Name}")
                return redirect("data_entry")
        except Exception as e:
            popup_message = f"Error: {e}"
    return render(request, "data_entry.html", {
        "residents": residents,
        "incident_choices": INCIDENT_CHOICES,
        "location_choices": INCIDENT_LOCATION_CHOICES,
        "popup_message": popup_message,
    })


# ---------- RESIDENT DETAILS ----------
def resident_details(request):
    residents = ResidentModel.objects.prefetch_related("resident_health_set").order_by("-id")
    return render(request, "resident_details.html", {"residents": residents})


#deleting residents
def delete_resident(request, resident_id):
    resident = get_object_or_404(ResidentModel, id=resident_id)
    resident.delete()
    return redirect("data_entry")




