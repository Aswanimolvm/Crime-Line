from django.db import models
from django.contrib.auth.hashers import make_password

class UserProfile(models.Model):
    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_admin = models.BooleanField(default=False)

    # Additional fields
    state = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    id_proof = models.CharField(max_length=50, blank=True, null=True)
    id_proof_number = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Hash password if not already hashed
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name



from django.db import models

class Complaint(models.Model):
    COMPLAINT_TYPES = [
        ('waste_dumping', 'Waste Dumping'),
        ('public_nuisance', 'Public Nuisance'),
        ('traffic_violations', 'Traffic Violations'),
        ('water_leakage', 'Water Leakage'),
        ('street_light', 'Street Light Issue'),
        ('noise_pollution', 'Noise Pollution'),
        ('illegal_construction', 'Illegal Construction'),
        ('stray_animals', 'Stray Animals'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    description = models.TextField()
    complaint_type = models.CharField(max_length=50, choices=COMPLAINT_TYPES)
    location = models.CharField(max_length=255)
    proof = models.FileField(upload_to='image/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  

    def __str__(self):
        return f"{self.get_complaint_type_display()} at {self.location}"



class Feedback(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    suggestion = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return f"Feedback from {self.user.full_name}"
