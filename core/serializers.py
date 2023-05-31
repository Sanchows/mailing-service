from django.utils import timezone
from rest_framework import serializers

from core.models import Client, Mailing, Code
from core.services.mailing import MailingService


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = "__all__"


class MailingSerializer(serializers.ModelSerializer):
    codes = CodeSerializer(many=True)

    class Meta:
        model = Mailing
        fields = "__all__"


class CreateMailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = (
            "name",
            "start_at",
            "end_at",
            "text",
            "tags",
            "codes",
        )

    def validate(self, data):
        if data["start_at"] > data["end_at"]:
            raise serializers.ValidationError({
                "error": "Дата начала должна быть раньше даты конца",
            })
        if data["start_at"] < timezone.now():
            raise serializers.ValidationError({
                "error": "Нельзя создать рассылку в прошлом",
            })

        return super(CreateMailingSerializer, self).validate(data)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        codes = validated_data.pop('codes')

        mailing = Mailing.objects.create(**validated_data)
        mailing.tags.add(*tags)
        mailing.codes.add(*codes)

        MailingService(mailing_instance=mailing).start_mailing(
            codes=codes,
            tags=tags
        )
        return mailing


class UpdateMailingSerializer(CreateMailingSerializer):
    pass


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = "__all__"


class CreateClientSerializer(ClientSerializer):
    pass
