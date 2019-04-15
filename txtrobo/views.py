from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from . import models

# Create your views here.
def index(request):
    return render(request, 'txtrobo/index.html')
