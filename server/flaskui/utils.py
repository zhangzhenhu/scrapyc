
def str2date(st):
    if not st:
        return None
    spl = st.replace(":"," ").replace("-"," ").split()
    return datetime(*[ int(x) for x in spl])
def str2int(v,default=None):
    v=v.strip()
    if not v:return default
    try:
        return int(v)
    except Exception, e:
        return  default


def str2dict(s):
    params = {}
    for line in  s.split("\n"):
        line = line.split("=",1)
        if len(line)  !=2 :
            continue
        params[line[0]] = line[1]
    return params
    