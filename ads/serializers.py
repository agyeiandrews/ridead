from django.conf import settings
from rest_framework import serializers

from driver.models import Driver
from driver.serializers import DriverSerializer
from rider.models import Rider
from rider.serializers import RiderSerializer
from user.models import User
from .models import Ad, AdInteraction, Reward

class AdSerializer(serializers.ModelSerializer):
    # ad_link = serializers.SerializerMethodField()
    custom_link  = serializers.URLField(required=False)
    viewed_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False)  # Handle the Many-to-Many
    
    # context data relate of rider
    rider = RiderSerializer(read_only=True)
    rider_id = serializers.PrimaryKeyRelatedField(queryset=Rider.objects.all(), source='rider')

    # context data relate of driver
    driver = DriverSerializer(read_only=True)
    driver_id = serializers.PrimaryKeyRelatedField(queryset=Driver.objects.all(), source='driver')
    class Meta:
        model = Ad
        fields = ['id', 'title', 'ad_link', 'target_country', 'target_location', 'target_region', 'show_time_start', 
        'show_time_end', 'timezone', 'to_be_viewed_by', 'content', 'numb_views', 'expiration_date', 
        'custom_link', 'expired', 'viewed_by', 'driver_id','rider_id', 'created_on', 'updated_on',
        'rider','driver']  # or specify the fields you want to include

    def get_ad_link(self, obj):
        if obj.ad_link:
            # Check if the media is a video or image and construct URLs accordingly
            if obj.ad_link.format in ['mp4', 'mov']:  # Assuming video files are in MP4 or MOV format
                return f"https://res.cloudinary.com/{settings.MEDIA_URL}/video/upload/{obj.ad_link.name}"
            return f"https://res.cloudinary.com/{settings.MEDIA_URL}/image/upload/{obj.ad_link.name}"
        return None


class AdInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdInteraction
        fields = ['ad', 'rider']  # Include fields as necessary

class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ['rider', 'driver', 'amount', 'created_at']  # Include fields as necessary
