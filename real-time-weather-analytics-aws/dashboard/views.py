from django.shortcuts import render
from django.http import HttpResponse
from .services.athena_service import get_latest_weather


def home(request):
    data = get_latest_weather()

    return render(request, "dashboard/home.html", {
        "data": data
    })