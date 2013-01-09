#!/usr/bin/env python

import os
PROJDIR = os.path.abspath(os.path.dirname(__file__))
ROOTDIR = os.path.split(PROJDIR)[0]
CONFDIR = os.path.join(PROJDIR, '_config')


from flask import Flask
from flask import render_template
from utils import import_object


app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)


def register(blueprint, url_prefix=None):
    """blueprint structure:

        {{blueprint}}/
            __init__.py
            models.py
            views.py
    """

    if url_prefix is None:
        url_prefix = '/%s' % blueprint

    views = import_object('%s.views' % blueprint)
    app.register_blueprint(views.app, url_prefix=url_prefix)
    return app


def prepare_app():
    register('search')
    register('detail')
    register('vodplay')
    register('transfer')
    register('m')
    register('page')
    register('api')
    return app

@app.route('/')
def hello():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.config.from_pyfile(os.path.join(CONFDIR, 'devconfig.py'))
    prepare_app()
    app.run(host='0.0.0.0')
