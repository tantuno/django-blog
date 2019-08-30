from celery import shared_task
from django.core.mail import EmailMessage, send_mail
from dev.celery import celery_app
from django.conf import settings

@shared_task
def hello(text):
    print('Hello there!')

@shared_task
def adding_task(x, y):
    return x + y

@celery_app.task
def send_mail_task(subject, message, to_email):
    # email = EmailMessage(subject, message, to=[to_email])
    # email.send()
    send_mail(subject, message, from_email=str(settings.EMAIL_HOST_USER), recipient_list=[to_email])
    # send_mail(subject, message, from_email='nazarvol17@gmail.com', recipient_list=[to_email])
