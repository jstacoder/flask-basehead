from flask import Flask, render_template,request,redirect,url_for,session,g
from flask.ext.codemirror import CodeMirror
from stars import get_starred_projects
from people import get_person
from forms import UserForm,CommentForm
from basecamp_tools import get_lens,get_current_todo_lists
from basecamp import BaseCamper, BC
from pagination import get_page
import datetime
from dateutil import parser as date_parser
from tools import datetimeformat


app = Flask(__name__)
app.config['SECRET_KEY'] = 'shjhhh'
app.config['CODEMIRROR_LANGUAGES'] = ['python','php','html']
app.config['CODEMIRROR_THEME'] = 'eclipse'
codemirror = CodeMirror(app)

def get_bc():
    bc = BaseCamper()
    return bc

bc = get_bc()
#@app.before_request
#def check_bc_creds():
#    if g.get('bc',None) is None:
#        return render_template('need_login.html')
#    else:
#        #user = g.get('bc',None).get('name',None)
#        #account = g.get('bc',None).get('account',None)
#        #passwd = g.get('bc',None).get('passwd',None)
#        #        g.bc = BaseCamper(account,user,passwd)
#        return redirect(url_for('index'))

def get_people():
    return bc.get_people()

def get_events():
    return bc.events

def get_projects():
    return bc.projects

def get_todos():
    return bc.current_todos

def get_todo_lists():
    return bc.todos

def get_event(i):
    for itm in bc.events:
        if itm['id'] == i:
            return itm
def get_attachments():
    return g.get('attachments',[])


def get_items(item):
    item_map = {
            'people':get_people,
            'todos':get_todos,
            'todo_lists':get_todo_lists,
            'attachments':get_attachments,
            #'docs':get_docs,
            'projects':get_projects,
            'events':get_events,
        }
    return item_map[item]()

@app.route('/profile/<int:userid>')
@app.route('/profile')
def profile(userid=None):
    if userid is None:
        person = bc.me
        starred = get_starred_projects(BC)
    else:
        person = get_person(BC,userid)
        starred = get_starred_projects(BC)
    return render_template('profile.html',bc=bc,person=person,starred=starred)

@app.route('/comment/<int:commentid>')
@app.route('/comment')
def comment(taskid=None):
    form = CommentForm()
    return render_template('comments.html',form=form,bc=bc)

@app.route('/test')
def test():
    tasks = get_todos()
    return render_template('task_checks.html',tasks=tasks,bc=bc)

@app.route('/pages/<item>/<int:page_num>')
def pages(item,page_num=None):
    if page_num is None:
        page_num = 1
    PER_PAGE = 5
    if item == 'attachments':
        PER_PAGE = 10    
    items = get_items(item)
    paginator = bc.paginator(page_num,PER_PAGE,len(items),item)
    page = paginator.get_page(items)
    return render_template('pages.html',page=page,bc=bc,items=items,p=paginator)

@app.route('/attachments/<path:url>/<int:page_num>')
@app.route('/attachments/<path:url>')
def attachments(url,page_num=None):
    atts = bc.send_basecamp_request(url)
    g.attachments = atts
    PER_PAGE = 10
    if page_num is None:
        page_num = 1
    paginator = bc.paginator(page_num,PER_PAGE,len(atts),'attachments',url=url)
    page = paginator.get_page(atts)
    return render_template('events.html',bc=bc,atts=page,p=paginator)

@app.route('/projects/<int:project_id>')
@app.route('/projects')
def projects(project_id=None):
    projects = bc.projects
    if project_id is None:
        return render_template('project_list.html',bc=bc,projects=projects)
    else:
        project = bc.get_project(project_id)
        return render_template('project_list.html',bc=bc,project=project,projects=projects)

@app.route('/reload')
def reload():
    bc = BaseCamper(**session['bc_instance'])
    return redirect(url_for(request.args['next']))

@app.route('/')
def index():
    return render_template('index.html',bc=bc)

@app.route('/tasks/<int:taskid>')
@app.route('/tasks')
def tasks(taskid=None):
    lists = bc.todo_lists[0]
    tasks = bc.current_todos
    buckets = bc.todo_buckets
    keys = buckets[0][0].keys()
    if taskid is None:
        return render_template('tasks.html',tasks=tasks,buckets=buckets,bc=bc,keys=keys,lists=lists)
    else:
        try:
            task = bc.get_todo_by_id(taskid)
            lst,nxt = bc.get_lst_nxt(taskid) 
        except:
            task = 'That todo does not exist'
            lst,nxt =  bc.get_lst_nxt(taskid) 
        return render_template('ttask.html',taskid=taskid,task=task,bc=bc,keys=keys,lst=lst,nxt=nxt)




@app.route('/tasklists')
def tasklists():
    # showing all lists / by bucket
    lists = bc.current_todos
    buckets = get_current_todo_lists(bc)
    bkt_lens = get_lens(buckets)
    return render_template('task_lists.html',buckets=buckets,bc=bc,bl=bkt_lens)
    


@app.route('/project_list')
def project_list():
    buckets = bc.todolists_by_project
    bkt_lens = get_lens(buckets)
    return render_template('project_task_list.html',buckets=buckets,bc=bc)

@app.route('/todolist/<int:idnum>')
@app.route('/todolist')
def todolist(idnum=None):
    if idnum is None:
        todolists = bc.todo_lists
        return render_template('todolist.html',bc=bc,todos=todolists)
    todolist = bc.get_todo_list(idnum)
    return render_template('todolist.html',bc=bc,tdl=todolist)


@app.route('/events/<int:event_id>')
@app.route('/events')
def events(event_id=None):
    if event_id is None:
        user = bc.name
        events = bc.events
        return render_template('event.html',events=events,user=user,bc=bc,body_style="padding:80px;")
    else:
        try:
            event = get_event(event_id)
            if event is None:
                event = 'No event loaded'
        except IOError:
            raise Exception('event failure')
        return render_template('event.html',event=event,bc=bc)


@app.template_filter('date')
def _filter_datetime(date,fmt=None):
    if date is None:
        return 
    date = date_parser.parse(str(date))
    if fmt:
        rtn = date.strftime(fmt)
    else:
        rtn = date.strftime('%m/%d/%y')
    return rtn
app.jinja_env.filters['date'] = _filter_datetime

def get_human_time(timestamp):
    import dateutil.parser as p
    d = p.parse(str(timestamp))
    return datetimeformat(datetime.datetime(d.year,d.month,d.day))
app.jinja_env.filters['human_time'] = get_human_time

@app.route('/people/<int:page>')
@app.route('/people')
def people(page=None):
    if page is None:
        page = 1
    return redirect(url_for('pages',item='people',page_num=page))


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8085)

