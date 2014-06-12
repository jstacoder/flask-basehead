# coding: utf-8
from core import send_request,make_api_url
try:
    from MY_BC import BC
except ImportError:
    BC = 2361076

def get_all_people(account_num=BC):
    return send_request(make_api_url(account_num,'people'))

def get_person(account_num=BC,person_id=None):
    if person_id is None:
        raise IOError('need a person to get')
    return send_request(make_api_url(account_num,'people',person_id))

def get_me(account_num=None):
    if account_num is None:
        account_num = BC
    return send_request(make_api_url(account_num,'people','me'))
