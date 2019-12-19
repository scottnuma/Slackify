from celery import Celery


def make_celery():
    return Celery("ensemble", broker="amqp://localhost")


celery = make_celery()
