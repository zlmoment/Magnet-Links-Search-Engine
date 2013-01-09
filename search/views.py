# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import render_template, flash
from flask import request

import urllib2
import json

app = Blueprint('search', __name__)


@app.route('/', methods=['GET'])
@app.route('', methods=['GET'])
def searchindex():
    return render_template("/search/index.html")

@app.route('/s/', methods=['GET'])
@app.route('/s', methods=['GET'])
def search():
    searchword = request.args.get('kw', '')
    page = request.args.get('page', '1')
    if searchword == "" or page == "":
        flash(u"亲，搜索词不能为空哦~")
        return render_template("index.html")
    result = {}
    result["searchword"] = searchword
    url = "http://torrentproject.com/?s="+searchword+"&start="+str(int(page)-1)+"&orderby=best&out=json"
    url=url.encode('utf-8')
    url=urllib2.unquote(url)
    f = urllib2.urlopen(url)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    result["total"] = int(parsed_json['total_found'])
    result["total_pages"] = int(result["total"])/50 + 1
    result["current_page"] = int(page)
    result_list = []
    for ob in parsed_json:
        if ob == "total_found":
            pass
        else:
            result_list.append(parsed_json[ob])
    result_list = sorted(result_list, key=lambda x:x['leechs'], reverse=True)
    result["list"] = enumerate(result_list)
    return render_template("/search/search_list.html", result = result, kw = searchword)