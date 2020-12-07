import json
from django.http import JsonResponse
from django.views import View
from .models import User
from utils.response import CommonResponseMixin, ReturnCode
from utils.auth import c2s, already_authorized

def get_staus(request):
    if already_authorized(request):
        data = {"is_authorized": 1}
    else:
        data = {"is_authorized": 0}
    response = CommonResponseMixin.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)

def logout(request):
    request.session.clear()
    response = {}
    response['result_code'] = 0
    response['message' ] = 'logout success'
    return JsonResponse(data=response, safe=False)
class UserView(View, CommonResponseMixin):
    def get(self, request):
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.SUCCESS)
            return JsonResponse(data=response, safe=False)
        open_id = request.session.get('open_id')
        user = User.objects.get(open_id=open_id)
        data = {}
        data['focus'] = {}
        data['focus']['city'] = json.loads(user.focus_city)
        data['focus']['cropId'] = json.loads(user.focus_cropId)
        response = self.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
        return JsonResponse(data=response, safe=False)

    def post(self, request):
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.SUCCESS)
            return JsonResponse(data=response, safe=False)
        open_id = request.session.get('open_id')
        user = User.objects.get(open_id=open_id)

        received_body = request.body.decode('utf-8')
        received_body = eval(received_body)

        city = received_body.get('city')
        cropId = received_body.get('cropId')

        user.focus_city = json.dumps(city)
        user.focus_cropId = json.dumps(cropId)
        user.save()

        response = self.wrap_json_response(code=ReturnCode.SUCCESS, message='modify user info success.')
        return JsonResponse(data=response, safe=False)
def __authorize_by_code(request):
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)
    code = post_data.get('code').strip()
    app_id = post_data.get('appId').strip()
    nickname = post_data.get('nickname').strip()

    response = {}
    if not code or not app_id:
        response['message'] = 'authorized failed, need entire authorization data.'
        response['code'] = ReturnCode.BROKEN_AUTHORIZED_DATA
        return JsonResponse(data=response, safe=False)
    data = c2s(app_id, code)
    openid = data.get('openid')
    print('get openid: ', openid)
    if not openid:
        response = CommonResponseMixin.wrap_json_response(code=ReturnCode.FAILED,message='auth failed')
        return JsonResponse(data=response, safe=False)
    request.session['open_id'] = openid
    request.session['is_authorized'] = True

    if not User.objects.filter(open_id=openid):
        new_user = User(open_id=openid, nicknaame=nickname)
        print('new user: open_id: %s, nickname: %s' % (openid, nickname))
        new_user.save()

    response = CommonResponseMixin.wrap_json_response(code=ReturnCode.SUCCESS, message='auth success.')
    return JsonResponse(data=response, safe=False)
    pass


def authorize(request):
    return __authorize_by_code(request)
