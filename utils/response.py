class ReturnCode:
    SUCCESS = 0
    FAILED = -100
    UNAUTHORIZED = -500
    BROKEN_AUTHORIZED_DATA = -501
    WRONG_PARAMS = -101

    @classmethod
    def message(cls, code):
        if code == cls.SUCCESS:
            return 'success'
        elif code == cls.FAILED:
            return 'failed'
        elif code == cls.UNAUTHORIZED:
            return 'unauthorized'
        elif code == cls.WRONG_PARAMS:
            return 'wrong params'

def wrap_json_response(data=None, code=None, message=None):
    response = {}
    if not code:
        code = ReturnCode.SUCCESS
    if not message:
        mesage = ReturnCode.message(code)
    if data:
        response['data'] = data
    response['result_code'] = code
    response['message'] = message
    return response

class CommonResponseMixin(object):
    @classmethod
    def wrap_json_response(cls, data=None, code=None, message=None):
        response = {}
        if not code:
            code = ReturnCode.SUCCESS
        if not message:
            mesage = ReturnCode.message(code)
        if data:
            response['data'] = data
        response['result_code'] = code
        response['message'] = message
        return response

