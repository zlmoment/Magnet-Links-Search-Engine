# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import render_template,request
import re,urllib2
import json
from utils import createShortLink,getConn


app = Blueprint('api', __name__)

@app.route('/', methods=['GET'])
@app.route('', methods=['GET'])
def api():
    return render_template("/api/index.html")

# http://mgnt.me/api/getresult?key=jyObEa&s=spiderman&page=1
@app.route('/getresult/', methods=['GET'])
@app.route('/getresult', methods=['GET'])
def getresult():
    apikey = request.args.get('key', '').lower()
    searchword = request.args.get('s', '').lower()
    page = request.args.get('page', '1')
    if apikey == "":
        return json.dumps([u"Please provide an apikey to access mgnt.me apis"])
    if apikey == "jyobea" and searchword != "spiderman":
        return json.dumps([u"This is a demo api, if you want full access, please contact mgnt.me to get an apikey."])
    if not checkapikey(apikey):
        return json.dumps([u"Invalid apikey, please contact mgnt.me"])
    else:
        addtimes(apikey)
        url = "http://torrentproject.com/?s="+searchword+"&start="+str(int(page)-1)+"&orderby=best&out=json"
        url=url.encode('utf-8')
        url=urllib2.unquote(url)
        f = urllib2.urlopen(url)
        json_string = f.read()
        return json_string

# http://mgnt.me/api/getshorturl?key=jyObEa&mag=magnet%3A%3Fxt%3Durn%3Abtih%3A0a84d05e9e1b426add4bd1166bfd5b311aee16ed%26dn%3DThe%20Amazing%20Spiderman%20%282012%29%20HDCAM%20x264%20AAC%20UNiQUE%26tr%3Dhttp%3A//121.14.98.151%3A9090/announce%26tr%3Dhttp%3A//bigtorrent.org%3A2710/announce%26tr%3Dhttp%3A//coppersurfer.tk%3A6969/announce%26tr%3Dhttp%3A//tracker1.wasabii.com.tw%3A6969/announce%26tr%3Dhttp%3A//www.h33t.com%3A3310/announce%26tr%3Dudp%3A//tracker.istole.it%3A80/announce%26tr%3Dudp%3A//tracker.publicbt.com%3A80/announce%26tr%3Dudp%3A//www.h33t.com%3A3310/announce
# original:
# magnet:?xt=urn:btih:0a84d05e9e1b426add4bd1166bfd5b311aee16ed&dn=The Amazing Spiderman (2012) HDCAM x264 AAC UNiQUE&tr=http://121.14.98.151:9090/announce&tr=http://bigtorrent.org:2710/announce&tr=http://coppersurfer.tk:6969/announce&tr=http://tracker1.wasabii.com.tw:6969/announce&tr=http://www.h33t.com:3310/announce&tr=udp://tracker.istole.it:80/announce&tr=udp://tracker.publicbt.com:80/announce&tr=udp://www.h33t.com:3310/announce
@app.route('/getshorturl/', methods=['GET'])
@app.route('/getshorturl', methods=['GET'])
def getshorturl():
    apikey = request.args.get('key', '').lower()
    maglink = urllib2.unquote(request.args.get('mag', '').lower())
    if apikey == "":
        return json.dumps([u"Please provide an apikey to access mgnt.me apis"])
    if apikey == "jyobea" and maglink != "magnet:?xt=urn:btih:0a84d05e9e1b426add4bd1166bfd5b311aee16ed&dn=The Amazing Spiderman (2012) HDCAM x264 AAC UNiQUE&tr=http://121.14.98.151:9090/announce&tr=http://bigtorrent.org:2710/announce&tr=http://coppersurfer.tk:6969/announce&tr=http://tracker1.wasabii.com.tw:6969/announce&tr=http://www.h33t.com:3310/announce&tr=udp://tracker.istole.it:80/announce&tr=udp://tracker.publicbt.com:80/announce&tr=udp://www.h33t.com:3310/announce".lower():
        return json.dumps([u"This is a demo api, if you want full access, please contact mgnt.me to get an apikey."])
    if not checkapikey(apikey):
        return json.dumps([u"Invalid apikey, please contact mgnt.me"])
    else:
        addtimes(apikey)
        regex=ur"magnet:\?.*"
        if not re.search(regex, maglink):
            return json.dumps([u"Invalid magnet link."])
        short_link = createShortLink(maglink)
        return json.dumps({"short_url":"http://mgnt.me/m/"+short_link})


def checkapikey(apikey):
    conn = getConn()
    conn.query("""select apikey from mgnt_apikey where apikey='%s';""" % apikey)
    result = conn.store_result().fetch_row()
    if result == ():
        return False
    else:
        return True
  
def addtimes(apikey):
    conn = getConn()
    conn.query("""update mgnt_apikey set times=times+1 where apikey='%s'""" % apikey)
      
        
        