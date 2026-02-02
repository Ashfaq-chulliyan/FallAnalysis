from django.db import models
# ---------- CHOICES ----------
INCIDENT_CHOICES = [
    ('LI', 'Leg Injury'),
    ('HI', 'Head Injury'),
    ('AI', 'Arm Injury'),
    ('BI', 'Back Injury'),
    ('FI', 'Fracture'),
    ('SP', 'Sprain'),
    ('BR', 'Bruise'),
    ('CT', 'Cut / Laceration'),
    ('KN', 'Knee Injury'),
    ('HP', 'Hip Injury'),
    ('SH', 'Shoulder Injury'),
    ('NK', 'Neck Injury'),
    ('FA', 'Fall No Injury'),
    ('OT', 'Other'),
]

INCIDENT_LOCATION_CHOICES = [
    ('RM', 'Resident Room'),
    ('BR', 'Bathroom'),
    ('HL', 'Hallway'),
    ('ST', 'Staircase'),
    ('DN', 'Dining Area'),
    ('GD', 'Garden / Outdoor'),
    ('LB', 'Lobby'),
    ('EL', 'Elevator'),
    ('WD', 'Ward'),
    ('NR', 'Nurse Station'),
    ('PT', 'Physiotherapy Room'),
    ('OT', 'Other'),
]

# ---------- RESIDENT ----------
class resident_detail(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    Resident_Name = models.CharField(max_length=25)
    Resident_Age = models.PositiveIntegerField()
    Resident_ID = models.PositiveIntegerField(unique=True)
    Resident_Gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    Resident_DateOfBirth = models.DateField(null=True, blank=True)
    Resident_AdmissionDate = models.DateField(null=True, blank=True)
    
    Resident_Phone = models.CharField(max_length=15, null=True, blank=True)
    Resident_GuardianName = models.CharField(max_length=25, null=True, blank=True)
    Resident_GuardianPhone = models.CharField(max_length=15, null=True, blank=True)
    Resident_Photo = models.ImageField(upload_to='ResidentsImages', null=True, blank=True)

    def __str__(self):
        return f"{self.Resident_Name} ({self.Resident_ID})"


# ---------- HEALTH ----------
class Resident_Health(models.Model):
    resident = models.ForeignKey(resident_detail, on_delete=models.CASCADE, null=True, blank=True)

    Physical_condition = models.TextField(null=True, blank=True)
    History = models.TextField(null=True, blank=True)
    Medication = models.TextField(null=True, blank=True)
    Doctor_Name = models.CharField(max_length=25, null=True, blank=True)
    Doctor_Appointment = models.DateTimeField(null=True, blank=True)
    Doctor_Contact = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.Doctor_Name} → {self.resident.Resident_Name if self.resident else 'Unknown'}"


# ---------- INCIDENT ----------
class Incident(models.Model):
    Resident = models.ForeignKey(
        resident_detail,
        on_delete=models.CASCADE,
        related_name='incidents'
    )
    Health_Record = models.ForeignKey(
        Resident_Health,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incidents'
    )
    Incident_type = models.CharField(
        max_length=10,
        choices=INCIDENT_CHOICES
    )
    Incident_time = models.DateTimeField(null=True, blank=True)
    Incident_location = models.CharField(
        max_length=2,
        choices=INCIDENT_LOCATION_CHOICES
    )
    Injury_level = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.Resident.Resident_Name} - {self.Incident_type}"