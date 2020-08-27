import logging
from os import makedirs, urandom
from os.path import join

logger = logging.getLogger(__name__)

FILENAME = "secret_key.cfg"


def init_app(app):
    if not app.secret_key:
        app.config.from_pyfile(FILENAME, silent=True)

        if not app.secret_key:
            app.secret_key = secret = urandom(16)
            path = join(app.config.root_path, FILENAME)
            with open(path, 'w') as f:
                f.write("SECRET_KEY = %r\n" % secret)
            logger.debug("Wrote SECRET_KEY to %s", path)
