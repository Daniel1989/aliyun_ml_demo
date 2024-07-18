import json

from django.http import JsonResponse
import pynlpir


# Create your views here.
def parse(request):
    if request.method == 'POST':
        statement = json.loads(request.statement)
        pynlpir.open()
        data = pynlpir.segment(statement)
        return JsonResponse({
            "success": True,
            "data": data
        })
    else:
        return JsonResponse({
            "success": False
        })
