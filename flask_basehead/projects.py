# coding: utf-8
from core import make_api_url, send_request

def get_all_active_projects(account_num):
    return send_request(make_api_url(account_num,'projects'))

def get_all_archived_projects(account_num):
    return send_request(make_api_url(account_num,'projects','archived'))

def get_project(account_num,project_id):
    return send_request(make_api_url(account_num,'projects',project_id))

