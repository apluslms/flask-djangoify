
from os import makedirs, urandom
from os.path import join
from werkzeug.utils import import_string
from flask import current_app
import flask

from flask_djangoify.utils import set_if_exists, get_config_processor, JSONEncoder, invalid_request

NAVS_KEY = 'navs'
PRODUCTION = 'production'
DEVELOPMENT = 'development'
version = '1.0'


class Djangoify(object):
    def __init__(self, app=None, *args, **kwargs):
        if app is not None:
            self.init_app(app)

    def init_app(self, app, *args, **kwargs):
        kwargs.setdefault('instance_relative_config', True)
        kwargs.setdefault('template_folder', 'templates')
        static_folder = kwargs.pop('static_folder', 'static')
        app.__init__(*args, import_name='flask_djangoify', static_folder=None, **kwargs)
        app.json_encoder = JSONEncoder
        app.static_folder = static_folder
        if static_folder and app.env != PRODUCTION:
            app.add_url_rule(
                app.static_url_path + '/<path:filename>',
                endpoint='static',
                view_func=app.send_static_file,
            )

    @staticmethod
    def configure(filename='config.py', test_config=None, **defaults):
        # ensure the instance folder exists
        try:
            makedirs(current_app.instance_path)
        except OSError:
            pass

        # load configuration to Flask
        current_app.config.from_mapping(**defaults)
        if test_config is None:
            current_app.config.from_pyfile(filename, silent=True)
        else:
            current_app.config.from_mapping(test_config)
        # handle secret key
        if not current_app.secret_key:
            current_app.secret_key = secret = urandom(16)
            fn = join(current_app.config.root_path, filename)
            with open(fn, 'a') as f:
                f.write("SECRET_KEY = %r\n" % secret)
            print(" - wrote SECRET_KEY to %s" % fn)
        elif isinstance(current_app.secret_key, str):
            current_app.secret_key = current_app.secret_key.encode('utf-8')

    @staticmethod
    def register_blueprint(blueprint):
        print(blueprint)
        if not isinstance(blueprint, flask.Blueprint):
            # Find module
            if isinstance(blueprint, str):
                module = import_string(blueprint)
            elif hasattr(blueprint, '__file__'):
                module = blueprint
            else:
                raise ValueError("blueprint must be Blueprint, module or string")

            # Find blueprint
            bps = [(n, b) for n, b in module.__dict__.items() if isinstance(b, flask.Blueprint)]
            if len(bps) != 1:
                raise ValueError(
                    "Couldn't find single Blueprint from %s, found %d: %s" % (len(bps), ', '.join((n for n, b in bps))))
            blueprint = bps[0][1]

        # set some path stuff
        set_if_exists(blueprint, 'static_folder', 'static')
        set_if_exists(blueprint, 'template_folder', 'templates')

        static = blueprint.static_folder
        if current_app.env == PRODUCTION:
            blueprint.static_folder = None

        current_app.register_blueprint(blueprint)

        if current_app.env == PRODUCTION:
            blueprint.static_folder = static

    def load_apps(self):
        for bp_mod in current_app.config.get('APPS', []):
            print(bp_mod)
            self.register_blueprint(bp_mod)

    @staticmethod
    def finalize_create():
        # connect nav list to contextprosesso
        print(current_app)
        current_app.config['apps'] = frozenset([x.name for x in current_app.blueprints.values()])
        # self.configure(get_config_processor(current_app))


        # static stuff for production
        if current_app.env == PRODUCTION:
            # Add static handlers so url_for works
            for bp in current_app.blueprints.values():
                current_app.add_url_rule('/static/<path:filename>', endpoint='%s.static' % (bp.name,), view_func=invalid_request)
            current_app.add_url_rule('/static/<path:filename>', endpoint='static', view_func=invalid_request)

            # Load collect
            try:
                from flask_collect import Collect
                collect = Collect()
                collect.init_app(current_app)
            except ImportError:
                pass

    @staticmethod
    def wrap_middleware():
        wsgi = current_app.wsgi_app
        for mw in current_app.config.get('MIDDLEWARE', []):
            if isinstance(mw, str):
                mw = import_string(mw)
            wsgi = mw(wsgi)
        current_app.wsgi_app = wsgi
