# coding: utf-8
from projects import get_project
from projects import get_all_active_projects
from core import send_request,get_auth
proj['todolists']
class ProjectManager(object):
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
                return send_request(url=proj['todolists']['url'].auth=get_auth())
        return None
    
