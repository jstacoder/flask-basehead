# coding: utf-8
from core import make_api_url,send_request
from MY_BC import BC


def get_starred_projects(account_num=BC):
    return send_request(make_api_url(account_num,'stars'))
