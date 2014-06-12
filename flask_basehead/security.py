

def get_auth():
    a = open('auth.txt','r').readlines()
    a = [x.strip() for x in a]
    return tuple(a)


