# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import render_template

app = Blueprint('page', __name__)

@app.route('/', methods=['GET'])
@app.route('', methods=['GET'])
@app.route('/about', methods=['GET'])
@app.route('/about/', methods=['GET'])
def about():
    return render_template("/page/about.html")

@app.route('/faq', methods=['GET'])
@app.route('/faq/', methods=['GET'])
def faq():
    return render_template("/page/faq.html")