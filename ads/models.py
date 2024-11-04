from django.db import models
from django.conf import settings
import uuid
from cloudinary.models import CloudinaryField

from driver.models import Driver

class Ad(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()  # Content of the ad
    video = CloudinaryField('video', folder='Advertisements', null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)  # Associate ad with driver
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ad {self.id}"

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
