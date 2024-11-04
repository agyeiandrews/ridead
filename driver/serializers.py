from rest_framework import serializers
from .models import Driver

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id','driver_id','full_name','date_of_birth', 'license_number', 
                  'vehicle_details','address','vehicle_type',
                    'onboarding_date','status']

    def create(self, validated_data):
        user = validated_data.pop('user')
        driver = Driver.objects.create(user=user, **validated_data)
        return driver
