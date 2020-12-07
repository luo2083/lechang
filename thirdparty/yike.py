import json
import requests
import evns

def yike(cityname):
    appid = evns.APPID
    appsecret = evns.APPSECRET
    api = 'https://www.tianqiapi.com/api/'
    params = 'appid=%s&appsecret=%s&cityname=%s' %(appid, appsecret, cityname)
    url = api + '?' + params
    response = requests.get(url=url)
    response = json.loads(response.text)
    print('yike return response is: ', response)
    return response

if __name__ == '__main__':
    data = yike('乐昌')