from rest_framework import serializers
from monitor.models import ThermalPoint, FireObject


class ThermalPointSerializer(serializers.ModelSerializer):

    class Meta:
        model = ThermalPoint
        fields = '__all__'


class FireObjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = FireObject
        fields = '__all__'