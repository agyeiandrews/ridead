from django.conf import settings
from django.db import models
import uuid
from django.utils import timezone

class Driver(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, blank=True, null=True)
    driver_id = models.CharField(max_length=20, unique=True, editable=False)
    license_number = models.CharField(max_length=100, unique=True)
    vehicle_details = models.CharField(max_length=255)
    onboarding_date = models.DateTimeField(auto_now_add=True)
    created_on = models.DateTimeField(default=timezone.now)
    date_of_birth = models.DateField(blank=True, null=True)  # Date of birth
    address = models.TextField(blank=True, null=True)  # Address
    # profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  # Use ImageField for Cloudinary
    vehicle_type = models.CharField(max_length=30, blank=True, null=True)  # Type of vehicle
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')  # Rider status

    def save(self, *args, **kwargs):
        if not self.driver_id:  # Only generate a new ID if it doesn't already exist
            current_year_month = timezone.now().strftime('%Y-%m')
            count = Driver.objects.filter(driver_id__startswith=f'DRIVER-{current_year_month}').count() + 1
            self.driver_id = f'DRIVER-{current_year_month}-{count:04}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.driver_id}"
