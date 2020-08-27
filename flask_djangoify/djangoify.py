from collections import OrderedDict
from contextlib import ExitStack
from os import makedirs, urandom
from os.path import join

import flask
from blinker import Namespace
from flask.app import setupmethod

from .utils import (
    get_config_processor,
    import_and_find_all,
    import_extension,
    set_if_exists,
)

PRODUCTION = 'production'
DEVELOPMENT = 'development'
version = '1.0'


class Djangoify(flask.Flask):
    def __init__(self, *args, **kwargs):
        # extra signals for this flask instance
        signals = Namespace()
        self.after_configure = signals.signal('after_configure')
        self.after_finalize = signals.signal('ofter_finalize')
        self.on_jinja_env = signals.signal('on_jinja_env')
        self.create_jinja_context = signals.signal('create_jinja_context')
        self.register_blueprint_context = signals.signal('register_blueprint_context')

        kwargs.setdefault('instance_relative_config', True)
        kwargs.setdefault('template_folder', 'templates')
        self.__extensions = extensions = [
            import_extension(ext) for ext in kwargs.pop('extensions', [])
        ]
        for ext in extensions:
            if hasattr(ext, 'prepare_app_kwargs'):
                ext.prepare_app_kwargs(kwargs)

        super().__init__(*args, static_folder=None, **kwargs)

        for ext in extensions:
            if hasattr(ext, 'prepare_app'):
                ext.prepare_app(self)


    @setupmethod
    def configure(self, filename='config.py', test_config=None, **defaults):
        # ensure the instance folder exists
        try:
            makedirs(self.instance_path)
        except OSError:
            pass

        # load configuration
        self.config.from_mapping(**defaults)
        if test_config is None:
            self.config.from_pyfile(filename, silent=True)
        else:
            self.config.from_mapping(test_config)

        # initialize extensions
        for ext in self.__extensions:
            if hasattr(ext, 'init_app'):
                ext.init_app(self)

        # clean configuration
        if isinstance(self.secret_key, str):
            self.secret_key = self.secret_key.encode('utf-8')

        # setup extensions
        self.after_configure.send(self)


    @setupmethod
    def finalize(self):
        # .before_first_request(f)

        # connect nav list to contextprosessor
        self.config['apps'] = frozenset([x.name for x in self.blueprints.values()])
        #self.context_processor(get_config_processor(self))

        # finalize extensions
        self.after_finalize.send(self)


    #@setupmethod - done by super()
    def register_blueprint(self, blueprint, **kwargs):
        # set some path stuff
        set_if_exists(blueprint, 'template_folder', 'templates')

        with ExitStack() as stack:
            for context in self.register_blueprint_context.receivers_for(self):
                stack.enter_context(context(self, blueprint))
            super().register_blueprint(blueprint, **kwargs)


    @setupmethod
    def register_blueprints(self, blueprints, **kwargs):
        for blueprint in import_and_find_all(blueprints, flask.Blueprint):
            self.register_blueprint(blueprint)


    def create_jinja_environment(self):
        env = super().create_jinja_environment()
        self.on_jinja_env.send(self, env=env)
        return env
