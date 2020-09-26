# Create your views here.
from django.http import Http404
from rest_framework.generics import ListAPIView

from monitor.models import ThermalPoint
from monitor.serializers import ThermalPointSerializer
from monitor.tasks import fetch_thermal_points_by_date_task

class ThermalPointView(ListAPIView):

    serializer_class = ThermalPointSerializer
    # Return all thermal points available in system

    def get_queryset(self):
        queryset = ThermalPoint.objects.all()
        if queryset.exists():
            return queryset
        else:
            raise Http404

    def get(self, request, *args, **kwargs):
        fetch_thermal_points_by_date_task()
        return self.list(request, *args, **kwargs)
