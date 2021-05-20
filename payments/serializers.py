from rest_framework import serializers

from .models import FaucetModel

class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = FaucetModel
        fields = ['status']

