from celery import Celery


def make_celery():
    return Celery("ensemble")


celery = make_celery()
