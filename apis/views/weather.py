import json
from django.http import JsonResponse
from django.views import View

from authorization.models import User
from thirdparty.yike import yike
from utils.response import CommonResponseMixin, ReturnCode
from utils.auth import already_authorized


class WeatherView(View, CommonResponseMixin):
    def get(self, request):
        if not already_authorized(request):
            response = self.wrap_json_response(data={}, code=ReturnCode.UNAUTHORIZED)
        else:
            open_id = request.session.get('open_id')
            user = User.objects.filter(open_id=open_id)[0]
            city = json.loads(user.focus_city)
            area =city['area']
            response = []
            area = area[:-1]
            data = yike(area)
            data['city_info'] = city
            response.append(data)
            response = self.wrap_json_response(data=response, code=ReturnCode.SUCCESS)
        return JsonResponse(data=response, safe=False)
    def post(self, request):
        received_body = request.body
        received_body = json.loads(received_body)
        city = received_body.get('city')
        response = []
        area = city['area']
        area = area[:-1]
        data = yike(area)
        data['city_info'] = city
        response.append(data)
        data = self.wrap_json_response(data=response)
        return JsonResponse(data=data, safe=False)