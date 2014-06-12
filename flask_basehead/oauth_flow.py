from requests_oauthlib import OAuth2Session



CLIENT_ID = 'acd90be92adf3a2d2c813d5e111c328af82cdd56'

CLIENT_SECRET = '565e575ebc47504d31baf49658c550f0e593efaf'

MY_RETURN_URL = 'http://174.140.227.137:8080/confirm' 

INIT_REQUEST_URL = 'https://launchpad.37signals.com/authorization/new'

TOKEN_REQUEST_URL = 'https://launchpad.37signals.com/authorization/token'


session = OAuth2Session(INIT_REQUEST_URL)
