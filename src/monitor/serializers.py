from rest_framework import serializers
from monitor.models import ThermalPoint


class ThermalPointSerializer(serializers.ModelSerializer):

    class Meta:
        model = ThermalPoint
        fields = '__all__'

