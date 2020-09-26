from django.shortcuts import render
from rest_framework.generics import ListAPIView
from monitor.serializers import ThermalPointSerializer
# Create your views here.


class ThermalPointView(ListAPIView):

    serializer_class = ThermalPointSerializer
    # Return all thermal points available in system

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
