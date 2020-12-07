import json
import logging
import sys
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from thirdparty.sts import Sts

from django.http import JsonResponse
from django.views import View

from .models import Images
import evns
from utils.auth import already_authorized, get_user
from utils.ml import get_ml
from utils.response import CommonResponseMixin, ReturnCode


logging.basicConfig(level=logging.INFO, stream=sys.stdout)

secret_id = evns.SECRET_ID     # 替换为用户的 secretId
secret_key = evns.SECRET_KEY      # 替换为用户的 secretKey
region = 'ap-guangzhou'     # 替换为用户的 Region
token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)


def get_sts(request):
    config = {
        'url': 'https://sts.tencentcloudapi.com/',
        'domain': 'sts.tencentcloudapi.com',
        # 临时密钥有效时长，单位是秒
        'duration_seconds': 1800,
        'secret_id': evns.SECRET_ID,
        # 固定密钥
        'secret_key': evns.SECRET_KEY,
        # 设置网络代理
        # 'proxy': {
        #     'http': 'xx',
        #     'https': 'xx'
        # },
        # 换成你的 bucket
        'bucket': 'lcagri-1304130461',
        # 换成 bucket 所在地区
        'region': 'ap-guangzhou',
        # 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的具体路径
        # 例子： a.jpg 或者 a/* 或者 * (使用通配符*存在重大安全风险, 请谨慎评估使用)
        'allow_prefix': '*',
        # 密钥的权限列表。简单上传和分片需要以下的权限，其他权限列表请看 https://cloud.tencent.com/document/product/436/31923
        'allow_actions': [
            # 简单上传
            'name/cos:PutObject',
            'name/cos:PostObject',
            # 分片上传
            'name/cos:InitiateMultipartUpload',
            'name/cos:ListMultipartUploads',
            'name/cos:ListParts',
            'name/cos:UploadPart',
            'name/cos:CompleteMultipartUpload'
        ],
    }
    try:
        sts = Sts(config)
        response = sts.get_credential()
        print('get data : ' + json.dumps(dict(response), indent=4))
        data = json.dumps(response)
        return JsonResponse(data=data,safe=False)
    except Exception as e:
        print(e)
        pass

class UrlView(View, CommonResponseMixin):
    def get(self, request):
        # if not already_authorized(request):
        #     response = self.wrap_json_response(code=ReturnCode.UNAUTHORIZED)
        #     return JsonResponse(data=response,safe=False)
        # user = get_user(request)
        # print('request user nickname is: ', user.nickname)
        # urls = user.image.all()
        # print('request.user.url is: ', urls)
        # response = []
        # for url in urls:
        #     item = get_ml(url)
        #     response.append(item)
        #     print('response is: ', response)
        # data = self.wrap_json_response(data=response)
        # print('return ml data is:', data)
        # return JsonResponse(data=data, safe=False)
        url = request.GET.get('url')
        crop_id = request.GET.get('crop_id')
        print('Return request url is:',url)
        data = get_ml(url, crop_id)
        response = self.wrap_json_response(data=data)
        print('return_ml response is:', response)
        return JsonResponse(data=response, safe=False)
    def post(self, request):
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.UNAUTHORIZED)
            return JsonResponse(data=response,safe=False)
        user = get_user(request)
        received_body = json.loads(request.body.decode('utf-8'))
        print(received_body)
        url = received_body.get('url')
        # for url in urls:
        #     image = Images.objects.create(url=url)
        #     image.user = user
        #     image.save()
        # data = self.wrap_json_response(code=ReturnCode.SUCCESS)
        print('new url is:', url)
        item = Images.objects.create(url=url)
        item.save()

        user.image.add(item)
        user.save()
        response = self.wrap_json_response(code=ReturnCode.SUCCESS)
        return JsonResponse(response, safe=False)

