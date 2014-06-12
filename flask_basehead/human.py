# coding: utf-8
def get_human_time(timestamp):
    import dateutil.parser as p
    d = p.parse(str(timestamp))
    return datetimeformat(datetime.datetime(d.year,d.month,d.day))