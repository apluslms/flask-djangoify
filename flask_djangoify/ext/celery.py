from celery import Celery
from celery.app.task import Task


def _setup(app):
    class ContextTask(Task):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super().__call__(*args, **kwargs)

    celery = Celery(app.import_name, task_cls=ContextTask)
    celery.config_from_object(app.config, namespace='CELERY')
    celery.autodiscover_tasks(app.config.get('APPS', []))

    app.extensions[__name__] = celery


def init_app(app):
   app.after_configure.connect(_setup)
