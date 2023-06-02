from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMessage

from core.models import Mailing


@shared_task
def send_daily_email():
    now = timezone.now()
    mailings = Mailing.objects.filter(end_at__gt=now - timedelta(days=1))

    context = {
        'mailings': mailings
    }
    body = get_template('daily_mail.html').render(context)
    message = EmailMessage(
        subject='Статистика по обработанным рассылкам',
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=[settings.EMAIL_HOST_USER, "dorozhko.margarita@gmail.com"],
    )
    message.content_subtype = "html"
    message.send()
