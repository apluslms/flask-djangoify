from flask_djangoify.utils import Blueprint

bp= Blueprint('test', __name__, url_prefix='/test')


@bp.route('/', methods=['GET', 'POST'])
def test_view():
    return 'hello test'
