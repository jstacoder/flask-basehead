from core import send_request
from people import get_me,get_all_people,get_person
from projects import get_all_active_projects, get_project
from todo_lists import get_todo_list, get_todo, get_all_active_todo_lists, get_todo_lists_for_person
from stars import get_starred_projects
from utils import Paginator

try:
    from MY_BC import BC
except ImportError:
    from core import MY_BC_NUMBER as BC

class Camper(object):
    def __init__(self,**kwargs):
        if kwargs.get('name',False):
            self.name = kwargs['name']
        if kwargs.get('id',False):
            self.id = kwargs['id']
        if kwargs.get('email_address',False):
            self.email_address = kwargs['email_address']
        if kwargs.get('admin',False):
            self.admin = kwargs['admin']
        if kwargs.get('created_at',False):
            self.created_at = kwargs['created_at']
        if kwargs.get('updated_at',False):
            self.updated_at = kwargs['updated_at']
        if kwargs.get('starred_projects',False):
            self._starred_projects = kwargs['starred_projects']
        if kwargs.get('active_projects',False):
            self._active_projects = kwargs['active_projects']
        if kwargs.get('events',False):
            self._events = kwargs['events']
        if kwargs.get('assigned_todos',False):
            self._assigned_todos = kwargs['assigned_todos']
        if kwargs.get('avatar_url',False):
            self.avatar_url = kwargs['avatar_url']
        if kwargs.get('fullsize_avatar_url',False):
            self.fullsize_avatar_url = kwargs['fullsize_avatar_url']
        self.todos = send_request(url=self._assigned_todos['url'])
        self.assigned_todos = []
        for bucket in self.todos:
            self.assigned_todos.append(bucket['assigned_todos'])
        self.all_todolists = get_todo_lists_for_person(BC,self.id)
        self.starred_projects = get_starred_projects(BC)
        self.events = send_request(url=self._events['url'])
        #self.active_projects = send_request(url=self._active_projects['url'])


    def get_avatar(self,filename):
        fp = open(filename,'wb')
        data = send_request(url=self.avatar_url,json=False)
        fp.write(data.content)
        fp.close()


class BaseCampPerson(object):
    BC_ACCOUNT_NUM = BC
    

class BaseCamper(BaseCampPerson):
    def __init__(self,bc_account_number=None,**kwargs):
        self.paginator = Paginator
        if bc_account_number is None and kwargs.get('account',None) is None:
            self.bc_number = self.BC_ACCOUNT_NUM
        else:
            if bc_account_number is not None:
                self.bc_number = bc_account_number
            else:
                self.bc_number = kwargs.get('account',None)

        self._internal_camper = Camper(**get_me(self.bc_number))
        self._todos = []
        for attr in dir(self._internal_camper):
            if not attr.startswith('_'):
                setattr(self,attr,getattr(self._internal_camper,attr))
        self._get_todos()
        
        self._get_projects()

    def __getitem__(self,key):
        if key in dir(self._internal_camper):
            return self._internal_camper.__dict__[key]

    def _get_todos(self):
        self._todo_buckets = []
        for bucket in self.assigned_todos:
            tmp = []
            for todo in bucket:
                res = send_request(url=todo['url'])
                tmp.append(res)
                self._todos.append(res)
            self._todo_buckets.append(tmp)

    def get_todo_list(self,idnum):
        for t in self.todo_lists:
            if t['id'] == idnum:
                return t

    def get_todo_by_id(self,idnum):
        for x in self.current_todos:
            if x['id'] == idnum:
                return x
        return None

    def get_lst_nxt(self,taskid):
        cur = None 
        last = None
        stop = False
        for x in self.current_todos:
            cur = x['id']
            if cur == taskid:
                stop = True
                continue
            if stop:
                return last, cur
            last = cur
        return last, None


    def get_todo_list_link(self,todolist_id):
        pass

    def get_project(self,pid):
        return get_project(self.BC_ACCOUNT_NUM,pid)

    def get_people(self,idnum=None):
        if idnum is None:
            rtn = get_all_people(self.BC_ACCOUNT_NUM)
        else:
            rtn = get_person(self.BC_ACCOUNT_NUM,idnum)
        return rtn

    def _get_projects(self):
        self.pm = BCProjectManager(self)

    @staticmethod
    def send_basecamp_request(url):
        return send_request(url=url)
    
    @property
    def me(self):
        return get_me(BC)


    @property
    def todo_lists(self):
        self._todo_lists = get_todo_lists_for_person(BC,self.id)
        return self._todo_lists

    @property
    def todolists_by_project(self):
        return sort_list_by_bucket(self.todo_lists)

    @property 
    def todo_buckets(self):
        return self._todo_buckets

    @property
    def current_todos(self):
        return self._todos

    @property
    def todo_count(self):
        return len(self._todos)

    @property
    def event_count(self):
        return len(self.events)
    @property
    def project_count(self):
        return len(self.projects)
    

    @property
    def projects(self):
        return self.pm.projects


class BCProjectManager(object):
    def __init__(self,camper):
        self.bc = camper
        self.projects = get_all_active_projects(self.bc.BC_ACCOUNT_NUM)

    def get_project(self,pid):
        return get_project(self.bc.BC_ACCOUNT_NUM,pid)

    def get_projects(self):
        return self.projects

    def get_project_todolists(self,pid):
        for proj in self.projects:
            if proj['id'] == pid:
                return send_request(url=proj['todolists']['url'])
        return None
    
def sort_list_by_bucket(lst):
    res = {}
    for itm in lst:
        if not res.get(itm['bucket']['name'],False):
            res[itm['bucket']['name']] = [itm]
        else:
            res[itm['bucket']['name']].append(itm)
    return res
# coding: utf-8
def sort_bucket_by_project(todo_lists):
    res = {}
    for itm in todo_lists:
        if not res.get(itm.get('bucket').get('name'),False):
            res[itm.get('bucket').get('name')] = [itm]
        else:
            res[itm.get('bucket').get('name')].append(itm)
    return res
