from datetime import timedelta
import uuid
from django.utils import timezone
import pytz

from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxLengthValidator, MinLengthValidator, RegexValidator
)
from django.db import models
from django.db.models.query import F, Q
from base.choices import BaseTextChoices


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Code(models.Model):
    label = models.CharField(
        primary_key=True,
        max_length=5,
        validators=[
            MinLengthValidator(
                limit_value=1,
                message="Код мобильного оператора должен быть не менее "
                        "1 символа"
            ),
            MaxLengthValidator(
                limit_value=5,
                message="Код мобильного оператора должен быть не более "
                        "5 символов"
            ),
            RegexValidator(
                regex=r"^\+[1-9][0-9]{1,3}$",
                message="Код мобильного оператора должен содержать символ '+' "
                        "в начале, и число от 1 до 9999",
            ),
        ]
    )

    def __str__(self):
        return self.label


class Tag(models.Model):
    label = models.CharField(
        primary_key=True,
        max_length=30,
        validators=[
            MinLengthValidator(
                limit_value=2,
                message="Тег должен быть не менее 2 символов"
            ),
            MaxLengthValidator(
                limit_value=30,
                message="Тег должен быть не более 30 символов"
            ),
        ]
    )

    def __str__(self):
        return self.label


class Mailing(BaseModel):
    class Status(BaseTextChoices):
        READY = "READY", "Ready"
        PROCESSING = "PROCESSING", "Processing"
        FINISHED = "FINISHED", "Finished"

    name = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    text = models.TextField()
    status = models.CharField(
        max_length=Status.max_length(),
        choices=Status.choices,
        default=Status.READY,
    )
    tags = models.ManyToManyField(Tag, related_name="mailing",)
    codes = models.ManyToManyField(Code, related_name="mailing",)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="mailing_start_before_end",
                check=Q(start_at__lt=F("end_at")),
            )
        ]

    def save(self, *args, **kwargs):
        if self.start_at > self.end_at:
            raise ValidationError("Дата начала должна быть раньше даты конца")
        if self.start_at < timezone.now():
            raise ValidationError("Нельзя создать рассылку в прошлом")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} | {self.start_at}"


class Client(BaseModel):
    tags = models.ManyToManyField(Tag, related_name="client",)

    code = models.ForeignKey(Code, on_delete=models.SET_NULL,
                             null=True, related_name="client")

    phone_number = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r"^7\d{10}$",
                message="Номер телефона должен быть в формате 7XXXXXXXXXX "
                        "(X - цифра от 0 до 9)",
            )
        ]
    )

    _available_timezones = pytz.common_timezones
    timezone = models.CharField(
        choices=((tz, tz) for tz in _available_timezones),
    )


class Message(models.Model):
    class Status(BaseTextChoices):
        SENDING = "SENDING", "Sending"
        SENT = "SENT", "Sent"
        FAILED = "FAILED", "Failed"

    created_at = models.DateTimeField(auto_now_add=True)
    mailing = models.ForeignKey(Mailing, on_delete=models.DO_NOTHING)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    status = models.CharField(
        max_length=Status.max_length(),
        choices=Status.choices,
        default=Status.SENDING,
    )
