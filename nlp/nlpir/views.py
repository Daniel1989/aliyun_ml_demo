import json

from django.http import JsonResponse
import pynlpir
from django.views.decorators.csrf import csrf_exempt


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
