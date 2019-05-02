from flask_djangoify import Djangoify
from flask_lti_login import lti, lti_login_authenticated

django_flask = Djangoify(__name__)
django_flask.configure(
    test_config=None,
    JWT_ALGORITHMS=['H256'],
    APPS=[
        'sample.test',
    ],
    MIDDLEWARE=[],
    USE_CDN=(django_flask.env == 'production')
)
django_flask.load_apps()
django_flask.wrap_middleware()
django_flask.finalize_create()

if __name__ == '__main__':
    django_flask.run()

