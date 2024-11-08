# user/authentication.py
from django.contrib.auth.backends import BaseBackend
from user.models import User  # Import your custom User model
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

class PhoneNumberBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, password=None):
        try:
            # Get the user by phone_number
            user = User.objects.get(phone_number=phone_number)
            if user.check_password(password):
                return user
            else:
                return None
        except ObjectDoesNotExist:
            return None
