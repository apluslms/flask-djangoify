from flask_djangoify import Djangoify


def create_app(test_config=None):
    app = Djangoify(__name__,
        extensions=[
            'flask_djangoify.ext.secret_key',
            'flask_djangoify.ext.views',
            'flask_djangoify.ext.proxy',
            'flask_djangoify.ext.middleware',
            'flask_djangoify.ext.proxy',
            'flask_djangoify.ext.cdn',
            'flask_djangoify.ext.celery',
            #'flask_collect.Collect',
        ],
    )
    print(" -- configure")
    app.configure(
        test_config=test_config,
        # defaults
        APPS=[
            'mysite',
        ],
        MIDDLEWARE=[],
        BEHIND_PROXY=False,
        USE_CDN=(app.env == 'production'),

        CELERY_RESULT_BACKEND="db+sqlite:///results.sqlite",
        CELERY_BROKER_URL="amqp://172.17.0.3/",
    )
    print(" -- finalize")
    app.finalize()
    print(" -- done")
    return app
