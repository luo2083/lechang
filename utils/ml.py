# -*- coding=utf-8
# appid 已在配置中移除,请在参数 Bucket 中带上 appid。Bucket 由 BucketName-APPID 组成
# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
import json
import ssl
import sys
import requests
import urllib
from urllib import request
from urllib.parse import urlencode
from urllib.request import urlopen


from lechang import settings
import evns
def get_ml(image, crop_id):
    print('image_url is: ', image)
    image_url = image
    host = 'https://senseagro.market.alicloudapi.com'
    path = '/api/senseApi'
    method = 'POST'
    appcode = evns.APPCODE
    querys = ''
    bodys = {}
    url = host + path

    bodys['crop_id'] = crop_id

    bodys['image_url'] = image_url
    print('bodys is : ', bodys)
    post_data = urlencode(bodys).encode('utf-8')
    print(post_data)
    result = urllib.request.Request(url, post_data)
    result.add_header('Authorization', 'APPCODE ' + appcode)
    # //根据API的要求，定义相对应的Content-Type
    result.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    response = urllib.request.urlopen(result, context=ctx)
    data = response.read()
    data = json.loads(data)
    if (data):
        print('ml return data is:', data)
    content = data.get('content')
    response = dict()
    response['msg'] = data['msg']
    response['status'] = data['status']
    response['result'] = content.get('result')
    response['score'] = content.get('score')
    return response

if __name__ == "__main__":
    data = get_ml(request)
