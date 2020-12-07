import json
import requests

import evns
from authorization.models import User
from utils import proxy


def already_authorized(request):
    is_authorized = False

    if request.session.get('is_authorized'):
        is_authorized = True
    return is_authorized

def get_user(request):
    if not already_authorized(request):
        raise Exception('Not authorized request.')
    else:
        open_id = request.session.get('open_id')
        user = User.objects.get(open_id=open_id)
        return user

def c2s(appid, code):
    API = 'https://api.weixin.qq.com/sns/jscode2session'
    params = 'appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % \
             (appid, evns.WX_APP_SECRET, code)
    url = API + '?' + params
    response = requests.get(url=url, proxies=proxy.proxy())
    data = json.loads(response.text)
    print(data)
    return data

