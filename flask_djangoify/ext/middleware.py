from werkzeug.utils import import_string


def wrap_wsgi_app(app):
    wsgi = app.wsgi_app
    for mw in app.config.get('MIDDLEWARE', []):
        if isinstance(mw, str):
            mw = import_string(mw)
        wsgi = mw(wsgi)
    app.wsgi_app = wsgi


def init_app(app):
    app.after_finalize.connect(wrap_wsgi_app)
