# coding: utf-8
def get_page(obj_list,per_page,page_num):
    s = ((per_page*page_num)-per_page)
    res = []
    total = 0
    while total != per_page:
        for i in range(per_page):
            try:
                res.append(obj_list[s])
            except:
                break
            finally:
                s+=1 
                total += 1
        break
    return res
