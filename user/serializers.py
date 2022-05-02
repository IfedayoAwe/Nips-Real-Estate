from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'is_realtor', ]
