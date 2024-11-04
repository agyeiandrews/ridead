from django.conf import settings
from rest_framework import serializers

from role.models import Role
from role.serializers import RoleSerializer
from .models import User, UserProfile
from rest_framework_simplejwt.tokens import RefreshToken

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'designation', 'additional_info']
        
class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    # image = serializers.ImageField(required=False)
    status = serializers.BooleanField()

    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), source='role')
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'first_name','last_name', 'phone_number', 'location',
                    'status','profile_picture','created_on', 'role_id', 'token']
        read_only_fields = ['created_on', 'status']
        extra_kwargs = {
            'password': {'write_only': True}  # Hide password field from responses
        }

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)
    
    def get_profile_picture(self, obj):
        if obj.profile_picture:
            # Construct the full Cloudinary URL
            return f"https://res.cloudinary.com/{settings.MEDIA_URL}/{obj.profile_picture.name}"
        return None



    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    new_password2 = serializers.CharField()