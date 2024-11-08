from django.contrib.auth.backends import ModelBackend
from .models import User

class PhoneNumberBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        try:
            # Attempt to find the user based on the phone_number
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return None  # Return None if user not found

        # Check the password against the hashed password stored in the database
        if user.check_password(password):
            return user
        return None  # Return None if the password is incorrect
