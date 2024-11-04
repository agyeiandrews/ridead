from django.conf import settings
from rest_framework import serializers
from .models import Ad, AdInteraction, Reward

class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'  # or specify the fields you want to include

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            # Construct the full Cloudinary URL
            return f"https://res.cloudinary.com/{settings.MEDIA_URL}/{obj.video.name}"
        return None

class AdInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdInteraction
        fields = ['ad', 'rider']  # Include fields as necessary

class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ['rider', 'driver', 'amount', 'created_at']  # Include fields as necessary
