# Create your views here.
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import View
from rest_framework.generics import ListAPIView
from data_extractor.client.cascade import extract_land_category_by_geo_tag
from monitor.models import ThermalPoint, FireObject
from monitor.serializers import ThermalPointSerializer, FireObjectSerializer
from monitor.tasks import fetch_thermal_points_by_date_task, fetch_fire_squares_by_date_task

class ThermalPointView(ListAPIView):

    serializer_class = ThermalPointSerializer

    def get_queryset(self):
        queryset = ThermalPoint.objects.all()
        if queryset.exists():
            return queryset
        else:
            raise Http404

    def get(self, request, *args, **kwargs):
        fetch_thermal_points_by_date_task()
        # fetch_fire_squares_by_date_task()
        return self.list(request, *args, **kwargs)


class FireObjectView(ListAPIView):

    serializer_class = FireObjectSerializer
    # Return all thermal points available in system

    def get_queryset(self):
        queryset = FireObject.objects.all()
        if queryset.exists():
            return queryset
        else:
            raise Http404

    def get(self, request, *args, **kwargs):
        # fetch_thermal_points_by_date_task()
        # fetch_fire_squares_by_date_task()
        return self.list(request, *args, **kwargs)
