from core import send_request, make_api_url
from MY_BC import BC

def update_todo(account_number,project_id,todo_id,todo_data):
    url = make_api_url(account_number,'projects',project_id,'todo',todo_id)
    return send_request(url,post_data=todo_data,post=True)


def make_todo_data(content=None,due_at=None,assignee=None,completed=None,old_data=None):
    data = {}

    if old_data:
        if content is None:
            data['content'] = old_data['content']
        if due_at is None:
            data['due_at'] = old_data['due_at']
        if assignee is None:
            data['assignee'] = old_data['assignee']
        if completed is None:
            data['completed'] = old_data['completed']
    else:
        data = {
        'content':content,
        'due_at':due_at,
        'assignee':assignee,
        'completed':completed
    }
    return data

print make_todo_data(content='crap',completed=False)
