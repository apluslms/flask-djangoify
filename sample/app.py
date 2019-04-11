from flask import Flask
from flask_djangoify import Djangoify


app = Flask(__name__)
with app.app_context():
    django_flask = Djangoify()
    django_flask.init_app(app=app)
    django_flask.configure(
        test_config=None,
        JWT_ALGORITHMS=['H256'],
        APPS=[
            'sample.test'
        ],
        MIDDLEWARE=[],
        USE_CDN=(app.env == 'production')
    )
    django_flask.load_apps()
    django_flask.wrap_middleware()
    django_flask.finalize_create()

if __name__ == '__main__':
    app.run()

