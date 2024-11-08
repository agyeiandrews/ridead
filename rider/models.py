from django.db import models
from django.conf import settings
import uuid
from django.utils import timezone

class Rider(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=50, blank=True, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True, null=True)
    rider_id = models.CharField(max_length=20, unique=True, editable=False, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    points = models.PositiveIntegerField(default=0)  # For rewards
    registration_date = models.DateTimeField(auto_now_add=True)
    created_on = models.DateTimeField(default=timezone.now)
    qr_code_url = models.URLField(blank=True, null=True)  # URL for the QR code 
    date_of_birth = models.DateField(blank=True, null=True)  # Date of birth
    address = models.TextField(blank=True, null=True)  # Address
    # profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  # Use ImageField for Cloudinary
    vehicle_type = models.CharField(max_length=30, blank=True, null=True)  # Type of vehicle
    license_number = models.CharField(max_length=50, blank=True, null=True)  # Driving license number
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')  # Rider status
    # bio = models.TextField(blank=True, null=True)  # Short biography
    updated_at = models.DateTimeField(auto_now=True)  # Last updated timestamp

    def save(self, *args, **kwargs):
        if not self.rider_id:  # Only generate a new ID if it doesn't already exist
            current_year_month = timezone.now().strftime('%Y-%m')
            count = Rider.objects.filter(rider_id__startswith=f'Rider-{current_year_month}').count() + 1
            self.rider_id = f'Rider-{current_year_month}-{count:04}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.rider_id}"
