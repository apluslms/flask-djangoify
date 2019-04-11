from collections import defaultdict
from decimal import Decimal
from os import makedirs, urandom
from os.path import exists, join
from werkzeug.utils import import_string
import flask


NAVS_KEY = 'navs'
PRODUCTION = 'production'
DEVELOPMENT = 'development'
version = '1.0'


class Namespace(dict):
    def __getattr__(self, key):
        try:
            return self.__getitem__(key)
        except KeyError:
            raise AttributeError("'%s'" % (key,))

    def __getitem__(self, *args, **kwargs):
        try:
            return super().__getitem__(*args, **kwargs)
        except KeyError:
            return []


class JSONEncoder(flask.json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super().default(o)


class Blueprint(flask.Blueprint):
    def nav(self, name, items):
        def add(state):
            navs = state.app.config.setdefault(NAVS_KEY, {})
            nav = navs.setdefault(name, [])
            nav.extend((('%s.%s' % (self.name, key), title) for key, title in items))
        self.record(add)


def set_if_exists(bp, var, value):
    if not getattr(bp, var, None):
        setattr(bp, var, value)
        if not exists(getattr(bp, var)):
            setattr(bp, var, None)


def get_config_processor(app):

    context = {
        'version': version,
        'use_cdn': app.config.get('USE_CDN', False),
        'apps': app.config['apps'],
        'navs': Namespace(app.config[NAVS_KEY]),
    }
    return lambda: context


def invalid_request(filename):
    return "Invalid", 500