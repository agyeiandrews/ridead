from django.db.models.signals import post_save
from django.dispatch import receiver

from driver.models import Driver
from rider.models import Rider
from user.models import User, UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


@receiver(post_save, sender=User)
def create_related_profile(sender, instance, created, **kwargs):
    if created:  # only run this when a new user is created
        role = instance.role
        if role:
            if role.name == "Rider":  # If the role is Rider
                Rider.objects.create(user=instance, full_name=instance.first_name)  # Adjust as necessary
            elif role.name == "Driver":  # If the role is Driver
                Driver.objects.create(user=instance, full_name=instance.first_name)  # Adjust as necessary