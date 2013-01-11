# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import render_template
from flask import request,flash, redirect

from utils import createShortLink

import re
import base64

app = Blueprint('vodplay', __name__)

@app.route('/', methods=['GET'])
@app.route('', methods=['GET'])
def vodplay():
    return render_template("/vodplay/index.html")

@app.route('/<source>/<title>', methods=['GET'])
@app.route('/<source>/<title>/', methods=['GET'])
#def play_prepare(source,title):
#    playid = base64.b64encode(source)
#    return render_template("/vodplay/play_prepare.html",playid = playid,title = title)
def playtvgua(source,title):
    url = "http://www.tvgua.com/vodtest.php?url="+source
    return redirect(url)


@app.route('/p/<playid>/<title>', methods=['GET'])
@app.route('/p/<playid>/<title>/', methods=['GET'])
def playwithcookie(playid,title):
    return render_template("/vodplay/play.html",playid = playid,title = title)

@app.route('/fromaddress', methods=['GET'])
def playfromadd():
    source = request.args.get('add', '')
    source = source.lower()
    if source == "":
        flash(u"亲~输入的资源地址不能为空！")
        return render_template("/vodplay/index.html")
    regex=[ur"thunder:.*",ur"http:.*",ur"ftp:.*",ur"magnet:.*",ur"ed2k:.*"]
    isright = False
    for r in regex:
        if re.search(r, source):
            isright = True
    if not isright:
        flash(u"亲~您输入的资源地址好像不对哦！")
        return render_template("/vodplay/index.html")
    else:
        #playid = base64.b64encode(source)
        #title = u"未知，内容资源来自用户输入"
        #return render_template("/vodplay/play_prepare.html",playid = playid,title = title)
        url = "http://www.tvgua.com/vodtest.php?url="+source
        return redirect(url)
    
@app.route('/fromhashid', methods=['GET'])
def playfromhashid():
    source = request.args.get('hashid', '')
    source = source.lower()
    if source == "":
        flash(u"亲~输入的资源不能为空！")
        return render_template("/vodplay/index.html")
    if len(source) != 40:
        flash(u"亲~您输入的特征值好像不对哦！")
        return render_template("/vodplay/index.html")
    else:
        source = "magnet:?xt=urn:btih:"+source
        #playid = base64.b64encode(source)
        #title = u"未知，内容资源来自用户输入"
        #return render_template("/vodplay/play_prepare.html",playid = playid,title = title)
        url = "http://www.tvgua.com/vodtest.php?url="+source
        return redirect(url)
        
        