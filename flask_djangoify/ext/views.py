def setup(app):
    for component in app.config.get('APPS', ()):
        app.register_blueprints(component + '.views')


def init_app(app):
    app.after_configure.connect(setup)
