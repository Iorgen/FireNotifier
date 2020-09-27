from django.urls import path

from fire_predictor.views import MainMapView

urlpatterns = [
    path('', MainMapView.as_view(), name='main-page'),
]