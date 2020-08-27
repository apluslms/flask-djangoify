from celery import shared_task
from flask import current_app


@shared_task
def add(x, y):
    print(current_app.config.get('APPS'))
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


