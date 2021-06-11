from rest_framework import serializers

from .models import Payment

class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ['status']
