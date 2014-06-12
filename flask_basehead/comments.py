from core import make_api_url, send_request, create_session,get_auth
import json

def get_session():
    sess = create_session()
    sess.auth = get_auth()
    return sess


def make_comment_content(txt,*subs):
    if len(subs) == 0:
        subs = [][:]
    return json.dumps(dict(content=txt,subscribers=subs))

def get_project_subscribers(account_num,project_id,name_list):
    return send_request(make_api_url(account_num,'projects',project_id,'accesses'),session=get_session())

def get_id_name_map(subs):
    res = {}
    for sub in subs:
        res[sub['name'].lower()] = sub['id']
    return res

def add_comment_to_todo(account_num,project_id,todo_id,content,*subs):
    url = make_api_url(account_num,'projects',project_id,'todos',todo_id,'comments')
    res = send_request(url,json=False,post=True,session=get_session(),data=make_comment_content(content,*subs))
    return res

TEST_DATA = [
        {
            "id": 149087659,
            "name": "Jason Fried",
            "email_address": "jason@basecamp.com",
            "updated_at": "2012-03-22T16:56:48-05:00",
            "url": "https://basecamp.com/999999999/api/v1/people/149087659-jason-fried.json"
        },
        {
            "id": 1071630348,
            "name": "Jeremy Kemper",
            "email_address": "jeremy@basecamp.com",
            "updated_at": "2012-03-22T16:56:48-05:00",
            "url": "https://basecamp.com/999999999/api/v1/people/1071630348-jeremy-kemper.json"
        }
]
