import json

from django.http import JsonResponse
import pynlpir
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import os
from django.core.files.base import ContentFile

from .bayes import get_classify, calc_prob
from .models import BayesResult


# Create your views here.

@csrf_exempt
def parse(request):
    if request.method == 'POST':
        statement = json.loads(request.body)["statement"]
        pynlpir.open()
        data = pynlpir.segment(statement)
        pynlpir.close()
        return JsonResponse({
            "success": True,
            "data": data
        })
    else:
        return JsonResponse({
            "success": False
        })


@csrf_exempt
def upload_bayes_datafile(request):
    file = request.FILES.get('file')
    if file and file.name.endswith('.csv'):
        default_storage.save(os.path.join('uploads', file.name), ContentFile(file.read()))
        data = calc_prob(os.path.join('uploads', file.name))
        os.remove(os.path.join('uploads', file.name))
        BayesResult.objects.create(PAb = data["PAb"], vocab=",".join(data["vocabSet"]), p1V=",".join([str(item) for item in data["p1V"]]), p0V=",".join([str(item) for item in data["p0V"]]))
        return JsonResponse({
            "success": True,
            "data": data
        })
    else:
        return JsonResponse({
            "success": False,
            "errorMsg": "上传文件失败"
        })


@csrf_exempt
def query_sentiment(request):
    if request.method == 'POST':
        statement = json.loads(request.body)["statement"]
        bayes = BayesResult.objects.order_by('-id').first()
        print(bayes.PAb)
        data = get_classify(statement, bayes.vocab.split(","), [float(item) for item in bayes.p1V.split(",")], [float(item) for item in bayes.p1V.split(",")], bayes.PAb)
        return JsonResponse({
            "success": True,
            "data": data
        })
    else:
        return JsonResponse({
            "success": False
        })
