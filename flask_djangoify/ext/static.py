from contextlib import contextmanager

from ..utils import set_if_exists


PRODUCTION = 'production'


def invalid_request(filename):
    return "Invalid", 500


def blueprint_static(func):

@contextmanager
def blueprint



def StaticFiles:
    def __init__(self):
        self.static_folder = None

    def prepare_app_kwargs(self, kwargs):
        self.static_folder = kwargs.pop('static_folder', 'static')

    def prepare_app(self, app):
        set_if_exists(app, 'static_folder', self.static_folder)

        if app.static_folder and app.env != PRODUCTION:
            app.add_url_rule(
                app.static_url_path + '/<path:filename>',
                endpoint='static',
                view_func=path.send_static_file,
            )

        app.register_blueprint = blueprint_static(app.register_blueprint)

        app.after_finalize.connect(self.finalize)

    def finalize(self, app):
        if app.env == PRODUCTION:
            # Add static handlers so url_for works
            for bp in app.blueprints.values():
                app.add_url_rule('/static/<path:filename>',
                                 endpoint='%s.static' % (bp.name,),
                                 view_func=invalid_request)
            app.add_url_rule('/static/<path:filename>',
                             endpoint='static',
                             view_func=invalid_request)

    @contextmanager
    def register_blueprint(self, app, blueprint):
        set_if_exists(blueprint, 'static_folder', self.static_folder)
        static = blueprint.static_folder
        if app.env == PRODUCTION:
            blueprint.static_folder = None
        yield
        if blueprint.static_folder is None:
            blueprint.static_folder = static


Extension = StaticFiles
