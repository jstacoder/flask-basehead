# coding: utf-8
def get_current_todo_lists(bc):
    ''' bc should be a BaseCamper object '''
    current = {}
    for itm in bc.assigned_todos:
        current[str(bc.get_todo_list(itm[0]['todolist_id'])['name'])] = []
        for x in itm:
            current[str(bc.get_todo_list(itm[0]['todolist_id'])['name'])].append(x)
            
    return current
    
def get_lens(c):
    rtn = {}
    for itm in c:
        rtn[itm] = len(c[itm])
    return rtn

