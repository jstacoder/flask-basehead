from core import make_api_url, get_auth, send_request

def get_all_topics(account_num):
    return send_request(make_api_url(account_num,'topics'),get_auth())

def get_project_topics(account_num,project_id):
    return send_request(make_api_url(account_num,'projects',project_id,'topics'),get_auth())


