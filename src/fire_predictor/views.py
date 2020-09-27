from django.views.generic import View
from django.shortcuts import render, redirect


class MainMapView(View):
    """
    Main page with custom map
    """
    template_name = 'fire_predictor/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

