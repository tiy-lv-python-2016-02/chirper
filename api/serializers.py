from chirps.models import Chirp
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    chirps = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'chirps')

class ChirpSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Chirp
        fields = '__all__'