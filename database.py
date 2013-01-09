import _mysql

def getConn():
    try:
        conn = _mysql.connect(host='localhost', user='root', passwd='', db='mgnt', port=3306)
    except Exception, e:
        print "Failed connection!", e
        return
    return conn