from django.core.mail import EmailMessage, send_mail
from dev.celery import celery_app
from django.conf import settings


@celery_app.task
def send_mail_task(subject, message, to_email):
    send_mail(subject, message = '', html_message=message,
              from_email=str(settings.EMAIL_HOST_USER), recipient_list=[to_email])
