import flask

NAVS_KEY = 'navs'


class Blueprint(flask.Blueprint):
    def nav(self, name, items):
        def add(state):
            navs = state.app.config.setdefault(NAVS_KEY, {})
            nav = navs.setdefault(name, [])
            nav.extend((('%s.%s' % (self.name, key), title) for key, title in items))

        self.record(add)


def finalize(app):
    navs = type('navs', (), app.config.get(NAVS_KEY, {}))
    def context_processor():
        return {'navs': navs}
    app.context_processor(context_processor)


def init_app(app):
    app.after_finalize.connect(finalize)
