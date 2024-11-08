from django.db import models
from django.conf import settings
import uuid
from cloudinary.models import CloudinaryField
from django.utils import timezone
from driver.models import Driver
from rider.models import Rider
from user.models import User

class Ad(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255,null=True, blank=True)  # Ad title, like "Melcom"
    ad_link = CloudinaryField('ad_link', folder='Advertisements', null=True, blank=True)  # Link to the media (image or video)
    target_country = models.CharField(max_length=255,null=True, blank=True)  # Target country
    target_location = models.CharField(max_length=255,null=True, blank=True)  # Specific location, e.g., "Accra"
    target_region = models.CharField(max_length=255,null=True, blank=True)  # Target region, e.g., "Greater Accra"
    show_time_start = models.TimeField(null=True, blank=True)  # Time when the ad should start showing
    show_time_end = models.TimeField(null=True, blank=True)  # Time when the ad should stop showing
    timezone = models.CharField(max_length=100,null=True, blank=True)  # Time zone
    to_be_viewed_by = models.IntegerField(default=0)  # The target number of views
    content = models.TextField(null=True, blank=True)  # Content of the ad
    numb_views = models.IntegerField(default=0,null=True, blank=True)  # The current number of views
    expiration_date = models.DateTimeField(null=True, blank=True)  # Date and time when the ad expires
    custom_link = models.URLField(null=True, blank=True)  # Optional link
    expired = models.BooleanField(default=False,null=True, blank=True)  # Whether the ad is expired
    viewed_by = models.ManyToManyField(User, related_name='viewed_ads', blank=True)  # Track users who viewed the ad
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE, related_name='ads',null=True, blank=True)  # Assuming this is a related model
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='ads',null=True, blank=True)  # Assuming this is a related model
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Ad {self.title}"

    def is_expired(self):
        """Check if the ad has expired based on the expiration date."""
        return timezone.now() > self.expiration_date

    def increment_view_count(self, user):
        """Add user to viewed_by and increment view count if not already viewed."""
        if not self.viewed_by.filter(id=user.id).exists():
            self.viewed_by.add(user)
            self.numb_views += 1
            self.save()

class AdInteraction(models.Model):
    rider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    reward_given = models.BooleanField(default=False)

    def __str__(self):
        return f"Interaction by {self.rider.username} on Ad {self.ad.id}"

class Reward(models.Model):
    rider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rider_rewards')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='driver_rewards')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    created_on = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f"Reward of {self.amount} for {self.rider.username} and {self.driver.username}"
