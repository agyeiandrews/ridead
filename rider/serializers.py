from rest_framework import serializers

from user.models import User
from user.serializers import UserSerializer
from .models import Rider



class RiderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user')
    class Meta:
        model = Rider
        fields = ['id','user_id','rider_id','full_name', 'points', 'registration_date','vehicle_type','license_number',
                   'date_of_birth','address','qr_code_url','status','user']
        read_only_fields = ['created_on', 'status']

    def create(self, validated_data):
        user = validated_data.pop('user')
        rider = Rider.objects.create(user=user,**validated_data)
        return rider
