from django.db.models import Q
from core.models import Client, Message, Mailing


class MessageService:
    @staticmethod
    def create_message(client_id, mailing_id):
        message = Message.objects.create(
            mailing=Mailing.objects.get(pk=mailing_id),
            client=Client.objects.get(pk=client_id),
        )
        return message

    @staticmethod
    def set_status_message_by_mailing_and_client(
        mailing_id, client_id, status: Message.Status
    ):
        message = Message.objects.get(
            mailing=Mailing.objects.get(pk=mailing_id),
            client=Client.objects.get(pk=client_id)
        )
        message.status = status
        message.save()

    @staticmethod
    def set_status_message_by_id(message_id, status: Message.Status):
        message = Message.objects.get(pk=message_id)
        message.status = status
        message.save()

    @staticmethod
    def get_unsent_messages_by_mailing_id(mailing_id):
        messages = Message.objects.filter(
            Q(mailing_id=mailing_id) & ~Q(status=Message.Status.SENT)
        )
        return messages
