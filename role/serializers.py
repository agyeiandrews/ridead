from rest_framework import serializers

from .models import Role

class RoleSerializer(serializers.ModelSerializer):

    status = serializers.BooleanField()

    class Meta:
        model = Role
        fields = ['id', 'name','status','description',
                 'created_on']
        read_only_fields = ['created_on']
