from rest_framework import serializers

from core.models import Message
from core.serializers import ClientSerializer, MailingSerializer


class MessageSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    mailing = MailingSerializer()

    class Meta:
        model = Message
        fields = "__all__"


class MessageClientByStatusSerializer(MessageSerializer):
    pass
