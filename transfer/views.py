# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import render_template, flash, redirect
from flask import request
import urllib2
import json

from BTL import BTFailure
import bencode
import hashlib

from utils import createShortLink

app = Blueprint('transfer', __name__)

@app.route('/t2m', methods=['GET'])
@app.route('/t2m/', methods=['GET'])
def indext2m():
    return render_template("/transfer/indext2m.html")

@app.route('/m2t', methods=['GET'])
@app.route('/m2t/', methods=['GET'])
def indexm2t():
    return render_template("/transfer/indexm2t.html")

@app.route('/upload', methods=['POST'])
def tor2mag():
    data = request.files['upload_file']
    if data:
        torrent = data.read()
        try:
            item={}
            metainfo = bencode.bdecode(torrent)
            info = metainfo['info']
            hashid=hashlib.sha1(bencode.bencode(info)).hexdigest()
            title=metainfo['info']['name']
            url = "http://torrentproject.com/"+hashid+"/trackers_json"
            url=url.encode('utf-8')
            url=urllib2.unquote(url)
            f = urllib2.urlopen(url)
            json_string = f.read()
            trackerJson = json.loads(json_string)
            maglink = "magnet:?xt=urn:btih:"+hashid+"&dn=" + urllib2.quote(title)
            for t in trackerJson:
                maglink += "&tr=" + t
            maglink += "&tr=http://tracker.openbittorrent.com/announce&tr=udp://tracker.openbittorrent.com:80/announce&tr=http://tracker.thepiratebay.org/announce&tr=http://tracker.publicbt.com/announce&tr=http://tracker.prq.to/announce&tr=udp://tracker.publicbt.com:80/announce"
            item["hashid"] = hashid
            item["maglink"] = maglink
            item["short_link"] = "http://mgnt.me/m/"+createShortLink(maglink)
            item["vodlink"] = urllib2.quote(u"/vodplay/magnet:?xt=urn:btih:")+hashid+"/"+urllib2.quote(title)
            return render_template("/transfer/indext2m.html",item = item)
        except BTFailure:
            flash(u"转换失败了...请重试...")
            return render_template("/transfer/indext2m.html")
    flash(u"出现未知错误，请重试...")
    return render_template("/transfer/indext2m.html")

@app.route('/upload/toplay', methods=['POST'])
def tor2play():
    data = request.files['upload_file']
    if data:
        torrent = data.read()
        try:
            metainfo = bencode.bdecode(torrent)
            info = metainfo['info']
            hashid=hashlib.sha1(bencode.bencode(info)).hexdigest()
            title=metainfo['info']['name']
            vodlink = urllib2.quote(u"/vodplay/magnet:?xt=urn:btih:")+hashid+"/"+urllib2.quote(title)
            return redirect(vodlink)
        except BTFailure:
            flash(u"转换种子文件失败了...请重试...")
            return render_template("/transfer/indext2m.html")
    flash(u"出现未知错误，请重试...")
    return render_template("/transfer/indext2m.html")