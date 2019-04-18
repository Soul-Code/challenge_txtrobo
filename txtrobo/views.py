from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Question, WorkFlow
from .classifier.Bayes.Bayes import Bayes
from .classifier.RandomForest.RandomForest import RFmodel

BAYES = 0
RANDOM_FOREST = 1
RANDOM_FOREST_2 = 2


# Create your views here.
def index(request):
    return render(request, 'txtrobo/index.html')


@csrf_exempt
def chat(request):
    if request.method == 'POST':
        txt_in = json.loads(request.body.decode()).get('txt', False)
        print(txt_in)

        bayes = Bayes()
        isok, result = bayes.use(txt_in)
        classified_result = sorted(result.items(), key=lambda i: i[1], reverse=True)
        print('isok:', isok)
        print('贝叶斯的结果哦：')
        for i in classified_result:
            print('%s:\t%.2f%%' % (i[0], i[1] * 100))
        if classified_result[0][1] > 0.5:
            # model_train(RANDOM_FOREST_1)
            # return HttpResponse('ok')
            rf = RFmodel()
            rf.loadModel()
            result1 = rf.use(txt_in)
            result2 = rf.use(txt_in, WorkFlow.objects.get(name=result1[0]))
            question = Question.objects.get(pk=result2[0])
            print('一级森林结果：\t', result1[0])
            print('二级森林结果：\t', question.value)
            return JsonResponse({'answer': question.answer.name})
        else:
            return JsonResponse({'answer': '不好意思我们的'})
    return HttpResponse('Only accept POST request.')


def model_train(model=BAYES):
    if model == BAYES:
        data_to_train = []
        # 从workflow表中获取类别
        class_list = [flow.name for flow in WorkFlow.objects.all()]
        # 从question表中获取训练数据
        for question in Question.objects.all():
            data_to_train.append([question.value, question.flow.name])
        # 导入模型进行训练~嘤~
        bayes = Bayes()
        bayes.load_data(data_to_train, class_list)
        bayes.train()

    elif model == RANDOM_FOREST:
        data_to_train = []
        # 从workflow表中获取类别
        class_list = [flow.name for flow in WorkFlow.objects.all()]
        # 从question表中获取训练数据
        for question in Question.objects.all():
            data_to_train.append([question.value, question.flow.name, question.id])
        rf = RFmodel()
        rf.load_data(class_list, data_to_train)
        rf.train()
        rf.saveModel()
