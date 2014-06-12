import datetime
from app import app

@app.template_filter('date')
def _filter_datetime(date,fmt=None):
    if fmt:
        rtn = date.strftime(fmt)
    else:
        rtn = date.strftime('%%m/%%d/%%Y')
    return rtn

