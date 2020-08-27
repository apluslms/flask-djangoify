def finalize(app):
    if app.config.get('BEHIND_PROXY', False):
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)


def init_app(app):
    app.after_finalize.connect(finalize)
