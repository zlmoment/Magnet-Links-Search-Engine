# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import render_template,request,flash
import re,urllib2

from utils import createShortLink, getConn

app = Blueprint('m', __name__)

@app.route('/', methods=['GET'])
@app.route('', methods=['GET'])
def m():
    return render_template("/m/index.html")

@app.route('/create', methods=['POST'])
def create():
    item = {}
    maglink = request.form['magnet']
    regex=ur"magnet:\?.*"
    if not re.search(regex, maglink):
        flash(u"亲，您输入的不是磁力链接哦~")
        return render_template("/m/index.html")
    else:
        item["short_link"] = createShortLink(maglink)
        return render_template("/m/index.html",item=item)

@app.route('/<surl>/', methods=['GET'])
@app.route('/<surl>', methods=['GET'])
def surl(surl):
    item = {}
    if len(surl) != 6:
        error = u"亲，您输入的段地址好像不对哦~"
        return render_template("/m/show.html", error = error)
    else:
        conn = getConn()
        conn.query("""select short_url,long_url from mgnt_url where short_url='%s';""" % surl)
        result = conn.store_result().fetch_row()
        if result == ():
            error = u"不好意思，没有找到此链接..."
            return render_template("/m/show.html", error = error)
        else:
            short_link = result[0][0]
            maglink = result[0][1]
        hashid = maglink[20:60]
        item["short_link"] = "http://mgnt.me/m/"+short_link
        item["maglink"] = maglink
        item["hashid"] = hashid
        item["vodlink"] = urllib2.quote(u"/vodplay/magnet:?xt=urn:btih:")+hashid+"/Unknown"
        return render_template("/m/show.html",item=item)

