from flask import render_template,request
from pdb import set_trace as _set_trace
from functools import wraps
import math
import datetime

#caching
def cached(app,timeout=5*60,key='view%s'):
    def decorator(f):
        @wraps(f)
        def wrapper(*args,**kwargs):
            cache_key = key % request.path
            rv = app.cache.get(cache_key)
            if rv is not None:
                return rv
            rv = f(*args,**kwargs)
            app.cache.set(cache_key,rv,timeout=timeout)
            return rv
        return wrapper
    return decorator

# template filters
def datetimeformat(value):
    delta = datetime.datetime.now() - value
    if delta.days == 0:
        formatting = 'today'
    elif delta.days < 10:
        formatting = '{0} days ago'.format(delta.days)
    elif delta.days < 20:
        formatting = '{0} weeks ago'.format(int(math.ceil(delta.days/7.0)))
    elif value.year == datetime.datetime.now().year:
        formatting = 'this year, on %d %b'
    else:
        formatting = 'on %b %d %Y'
    return value.strftime(formatting)


def set_trace():
    '''
    wrapper for pdb.set_trace
    '''
    if not app.debug:
        return 
    _set_trace()

def simple_form(form_type,template,success):
    def fn():
        form = form_type()
        if form.validate_on_submit():
            return success()
        return render_template(template,form=form)
    return fn

def row_to_dict(row):
    return dict((col,getattr(row,col)) for col in row.__table__.columns.keys())

def rows_to_dict(rows):
    return map(row_to_dict,rows)


