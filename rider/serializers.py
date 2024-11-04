from rest_framework import serializers
from .models import Rider

class RiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rider
        fields = ['id','rider_id','full_name', 'points', 'registration_date','vehicle_type','license_number',
                   'date_of_birth','address','qr_code_url','status']

    def create(self, validated_data):
        user = validated_data.pop('user')
        rider = Rider.objects.create(user=user, **validated_data)
        return rider
