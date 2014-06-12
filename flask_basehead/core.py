'''
    new_bc.core.py

    core api calls for new_bc api library
'''
import os
import requests 


API_URL = 'https://basecamp.com/{}/api/v1/'
MY_BC_NUMBER = '2361076'

def make_api_url(account_num=None,call=None,*args):
    if account_num is None:
        account_num = MY_BC_NUMBER
    if call is None:
        call = ''
    u = API_URL.format(account_num) + call 
    u = u + '.json' if not args else u + '/' + '/'.join(map(str,args)) + '.json'
    return u


def get_auth(username=None,passwd=None):
    if username and passwd:
        return (username,passwd)
    elif os.environ.get('BC_AUTH',False):
        return os.environ['BC_AUTH'].split(' ')
    else:
        if os.path.exists('auth.txt'):
            return tuple([str(x[:-1]) for x in tuple(open('auth.txt').readlines())])

def create_session(auth=None,oauth2=False):
    if not oauth2:
        req = requests.session()
    else:
        import os
        url = os.environ.get('INIT_REQUEST_URL',None)
        import requests_oauthlib
        req = requests_oauthlib.OAuth2Session(url)
    if auth is None:
        req.auth = get_auth()
    else:
        if len(auth) == 2:
            req.auth = get_auth(auth)
        else:
            raise IOError('unsupported authentication')
    return req

def send_request(url,json=True,post=False,session=None,**kwargs):
    if session is None:
        req = create_session()
    else:
        req = session
    if url is None:
        if kwargs == {}:
            raise IOError('need a url to send request to')
        else:
            account_num = kwargs.pop('account_num',None)
            call = kwargs.pop('call',None)
            args = kwargs.values()
            if args:
                url = make_api_url(account_num=account_num,call=call,*args)
            else:
                url = make_api_url(account_num=account_num,call=call)
    if not post:
        if json:
            return req.get(url).json()
        else:
            return req.get(url)
    else:
        data = kwargs.get('post_data',None)
        if json:
            return req.post(url,data=data).json()
        else:
            return req.post(url,data=data)
