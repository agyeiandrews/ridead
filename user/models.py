from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone
from django.conf import settings
from role.models import Role
from uuid import uuid4
import os
from cloudinary.models import CloudinaryField

# Create your models here.

# def upload_to_user(instance, filename):
#     extension = filename.split('.')[-1] if '.' in filename else 'jpg'  # Default to jpg if no extension
#     new_filename = f"{uuid4()}.{extension}"  # Generates a unique filename
#     return os.path.join('UserProfile', new_filename)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100, null=False, blank=False)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=50)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='users', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = CloudinaryField('profile_picture', folder='UserProfile', blank=True, null=True)  # Specify folder
    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.first_name or self.username
    
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)  # Biography
    designation = models.CharField(max_length=100, blank=True, null=True)  # Designation
    additional_info = models.JSONField(blank=True, null=True)  # Any additional info as JSON

    def __str__(self):
        return f"{self.user.username}'s Profile"