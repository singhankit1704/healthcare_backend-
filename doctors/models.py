from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('cardiologist', 'Cardiologist'),
        ('neurologist', 'Neurologist'),
        ('orthopedic', 'Orthopedic'),
        ('pediatrician', 'Pediatrician'),
        ('dermatologist', 'Dermatologist'),
        ('psychiatrist', 'Psychiatrist'),
        ('oncologist', 'Oncologist'),
        ('radiologist', 'Radiologist'),
        ('general', 'General Physician'),
        ('other', 'Other'),
    ]

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctors')
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES, default='general')
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20, blank=True)
    license_number = models.CharField(max_length=100, unique=True)
    experience_years = models.PositiveIntegerField(default=0)
    qualification = models.CharField(max_length=255, blank=True)
    hospital = models.CharField(max_length=255, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Dr. {self.name} ({self.get_specialization_display()})"
