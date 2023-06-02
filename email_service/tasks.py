from django.core.mail import send_mail
from celery import shared_task
from core.services.mailing import MailingService


@shared_task
def send_daily_email():
    # send_mail(
    #     'Тема письма',
    #     'Текст письма.',
    #     'from@example.com',
    #     ['to@example.com'],
    #     fail_silently=False,
    # )
    print('TASKAAAA')