# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import render_template
import urllib2
import json

from utils import createShortLink

app = Blueprint('detail', __name__)

@app.route('', methods=['GET'])
@app.route('/', methods=['GET'])
def detail():
    return render_template("/detail/single_result.html", error = True)


@app.route('/<hashid>/<title>/<size>/<seeds>/<leechs>')
@app.route('/<hashid>/<title>/<size>/<seeds>/<leechs>/')
def single_result(hashid,title,size,seeds,leechs):
    item = {}
    item["hashid"] = hashid
    item["title"] = title
    item["size"] = size
    item["seeds"] = seeds
    item["leechs"] = leechs
    if hashid == "":
        return render_template("/detail/single_result.html", error = True)
    # get tracker json list
    url = "http://torrentproject.com/"+hashid+"/trackers_json"
    url=url.encode('utf-8')
    url=urllib2.unquote(url)
    f = urllib2.urlopen(url)
    json_string = f.read()
    trackerJson = json.loads(json_string)
    maglink = "magnet:?xt=urn:btih:"+hashid+"&dn=" + urllib2.quote(title.encode('utf-8'))
    for t in trackerJson:
        maglink += "&tr=" + t
    maglink += "&tr=http://tracker.openbittorrent.com/announce&tr=udp://tracker.openbittorrent.com:80/announce&tr=http://tracker.thepiratebay.org/announce&tr=http://tracker.publicbt.com/announce&tr=http://tracker.prq.to/announce&tr=udp://tracker.publicbt.com:80/announce"
    item["maglink"] = maglink
    item["perm_link"] = "http://mgnt.me/detail/"+hashid+"/"+title+"/"+size+"/"+seeds+"/"+leechs
    item["short_link"] = "http://mgnt.me/m/"+createShortLink(maglink)
    item["vodlink"] = urllib2.quote(u"/vodplay/magnet:?xt=urn:btih:")+hashid+"/"+urllib2.quote(title.encode('utf-8'))
    return render_template("/detail/single_result.html", item = item)

