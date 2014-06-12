from math import ceil

class Paginator(object):
    def __init__(self,page,per_page,total_count,item=None,**kwargs):
        url = kwargs.get('url',False)
        if url:
            self.url = url
        self.item_type = item
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self,left_edge=2,left_current=2,
            right_current=5,right_edge=2):
        last = 0 
        for num in xrange(1,self.pages+1):
            if num <= left_edge or \
                    (num > self.page - left_current - 1 and \
                    num < self.page + right_current) or \
                    num > self.pages - right_edge:
                        if last + 1 != num:
                            yield None
                        yield num
                        last = num
    iter_all_pages = iter_pages
    
    def get_page(self,obj_list):
        s = ((self.per_page*self.page)-self.per_page)
        res = []
        total = 0
        while total != self.per_page:
            for i in range(self.per_page):
                try:
                    res.append(obj_list[s])
                except:
                    break
                finally:
                    s+=1 
                    total += 1
            break
        return res

