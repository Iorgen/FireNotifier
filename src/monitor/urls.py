from django.urls import path

from monitor.views import ThermalPointView, FireObjectView

urlpatterns = [
    path('thermal_points/', ThermalPointView.as_view()),
    path('fire_objects/', FireObjectView.as_view())
]