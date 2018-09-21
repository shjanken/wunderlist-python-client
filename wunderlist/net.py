'''
向 wunderlist 的 resutful api 发送请求
'''
import requests
import os

common_url = "https://a.wunderlist.com/api/v1/{}"


class WunderClientException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def read_envrion():
    '''
read the 'x-access-token' and 'x-client-id' from environment
    '''
    return {
        'X-Access-Token': os.environ.get('X_Access_Token', 'none'),
        'X-Client-ID': os.environ.get('X_Client_ID', 'none')
    }


def send_request(action, params={}):
    '''
    根据 action 来发送请求。
    action 是 restful api 的资源名字。比如： user, lists, tasks
    '''
    auth_headers = read_envrion()

    if auth_headers.get('X-Access-Token') == 'none' or auth_headers.get('X-Client-ID') == 'none':
        raise WunderClientException("""no 'token' or 'client id' environment. 
please set these environments first""")

    return requests.get(common_url.format(action), headers=auth_headers, params=params)
