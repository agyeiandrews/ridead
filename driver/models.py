from django.conf import settings
from django.db import models
import uuid
from django.utils import timezone

class Driver(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
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
     # Additional fields from the SQL schema
    todays_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    weekly_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    monthly_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overall_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sales_history = models.JSONField(default=dict,blank=True, null=True)  # Store sales history in JSON format
    customers = models.JSONField(default=list,blank=True, null=True)  # Store customers as a list of IDs
    target_location = models.CharField(max_length=255, blank=True, null=True)
    target_region = models.CharField(max_length=255, blank=True, null=True)
    target_country = models.CharField(max_length=255, blank=True, null=True)
    # user_type = models.CharField(max_length=50, default='driver')
    user_qrcode = models.URLField(blank=True, null=True)  # URL to the driver's QR code

    updated_at = models.DateTimeField(auto_now=True)  # Last updated timestamp

    def save(self, *args, **kwargs):
        if not self.driver_id:  # Only generate a new ID if it doesn't already exist
            current_year_month = timezone.now().strftime('%Y-%m')
            count = Driver.objects.filter(driver_id__startswith=f'DRIVER-{current_year_month}').count() + 1
            self.driver_id = f'DRIVER-{current_year_month}-{count:04}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.driver_id}"
