from django.shortcuts import render
from django.http import HttpResponse
from .services.athena_service import get_latest_weather
from django.http import JsonResponse


def home(request):
    return render(request, "dashboard/index.html")


def weather_api(request):
    weather = get_latest_weather()
    return JsonResponse(weather)