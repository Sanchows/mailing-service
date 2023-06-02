from django.core.mail import send_mail
from celery import shared_task
from core.services.mailing import MailingService
from django.conf import settings

@shared_task
def send_daily_email():
    message = MailingService.get_info_about_mailings()
    send_mail(
        subject='Статистика по обработанным рассылкам',
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.EMAIL_HOST_USER],
        fail_silently=False,
    )
