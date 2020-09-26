from django.urls import path

from monitor.views import ThermalPointView

urlpatterns = [
    #
    path('thermal_points/', ThermalPointView.as_view())

]