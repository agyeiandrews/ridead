from rest_framework import serializers

from user.models import User
from user.serializers import UserSerializer
from .models import Driver

class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user')
    class Meta:
        model = Driver
        fields = fields = [
            'id','user_id', 'driver_id', 'full_name', 'date_of_birth', 'license_number', 
            'vehicle_details', 'address', 'vehicle_type', 'onboarding_date', 
            'status', 'todays_revenue', 'weekly_revenue', 'monthly_revenue', 
            'overall_revenue', 'sales_history', 'customers', 'target_location',
            'target_region', 'target_country', 'user_qrcode', 'created_on', 'updated_at',
            'user'
        ]
        read_only_fields = ['created_on', 'status']

    def create(self, validated_data):
        user = validated_data.pop('user')
        driver = Driver.objects.create(user=user, **validated_data)
        return driver
