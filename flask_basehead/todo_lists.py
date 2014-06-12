from core import make_api_url, send_request

# active todos from project
def get_active_project_todo_lists(account_num,project_id):
    return send_request(make_api_url(account_num,'projects',project_id,'todolists'))

# complete todos for project
def get_complete_project_todo_lists(account_num,project_id):
    return send_request(make_api_url(account_num,'projects',project_id,'todolists','completed'))

# active todos for all projects
def get_all_active_todo_lists(account_num):
    return send_request(make_api_url(account_num,'todolists'))

# complete todos for all projects
def get_all_complete_todo_lists(account_num):
    return send_request(make_api_url(account_num,'todolists','completed'))

# get todolists assigned to person
def get_todo_lists_for_person(account_num,person_id):
    return send_request(make_api_url(account_num,'people',person_id,'assigned_todos'))

# get specific todolist, must specify project and todolist
def get_todo_list(account_num,project_id,todolist_id):
    return send_request(make_api_url(account_num,'projects',project_id,'todolists',todolist_id))

def get_todo(account_num,project_id,todo_id):
    return send_request(make_api_url(account_num,'projects',project_id,'todos',todo_id))

