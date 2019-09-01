import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dev.settings')

celery_app = Celery('dev')
celery_app.config_from_object('django.conf:settings', namespace='')
celery_app.autodiscover_tasks()
celery_app.conf.broker_url = 'redis://redis:6379'
