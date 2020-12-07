import os
import yaml

from django.http import JsonResponse
from lechang import settings
from utils.response import wrap_json_response, ReturnCode


def init_app_data():
    data_file = os.path.join(settings.BASE_DIR, 'app.yaml')
    with open(data_file, 'r', encoding='utf-8') as f:
        apps = yaml.load(f ,Loader=yaml.FullLoader)
        return apps

def get_menu(request):
    global_data = init_app_data()
    published_data = global_data.get('published')
    response = wrap_json_response(published_data, code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)


