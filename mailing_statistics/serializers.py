from rest_framework import serializers

from core.models import Message
from core.serializers import ClientSerializer, MailingSerializer


class StatisticsMessageSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    mailing = MailingSerializer()

    class Meta:
        model = Message
        fields = "__all__"
