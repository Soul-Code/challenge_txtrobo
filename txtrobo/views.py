from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .classifier.Bayes.Bayes import Bayes
from .classifier.RandomForest.RandomForest import RFmodel

BAYES = 0
RANDOM_FOREST_1 = 1
RANDOM_FOREST_2 = 2


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


def model_train(model=BAYES, trained_table=None):
    if model == BAYES:

        pass
    elif model == RANDOM_FOREST_1:
        pass
    elif model == RANDOM_FOREST_2:
        if trained_table:
            pass
        else:
            return False, '二级随机森林训练需要提供表对象'
        pass


def classify(txt_in):
    pass
