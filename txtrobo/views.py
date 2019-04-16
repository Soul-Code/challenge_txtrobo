from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.
def index(request):
    return render(request, 'txtrobo/index.html')


@csrf_exempt
def chat(request):
    if request.method == 'POST':
        txt_in = json.loads(request.body.decode()).get('txt', False)
        print(txt_in)
        return JsonResponse({'answer': '你好啊~'})
    return HttpResponse('Only accept POST request.')
