from datetime import datetime
from celery import Task, shared_task
from django.conf import settings
from django.utils import timezone
import httpx

from core.models import Mailing, Message
from core.services.client import ClientService
from core.services.message import MessageService
from core.services.exceptions import BadAuthToken, Response400Error


class SendMessageTask(Task):
    def on_success(self, return_value, task_id, args, kwargs):
        _, _, _, mailing_id = args
        message_id = return_value[1]
        MessageService.set_status_message_by_id(
            message_id=message_id,
            status=Message.Status.SENT
        )

        MailingService.set_finish_if_all_messages_have_been_done(
            mailing_id=mailing_id
        )

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        client_id, _, _, mailing_id = args
        MessageService.set_status_message_by_mailing_and_client(
            mailing_id=mailing_id,
            client_id=client_id,
            status=Message.Status.FAILED
        )

        MailingService.set_finish_if_all_messages_have_been_done(
            mailing_id=mailing_id
        )


@shared_task(base=SendMessageTask)
def send_message_task(client_id, phone_number, text, mailing_id):
    URL = "https://probe.fbrq.cloud/v1/send/"
    MAILING_SERVER_TOKEN = settings.PROBE_MAILING_SERVER_TOKEN

    message = MessageService.create_message(client_id, mailing_id)

    data = {
        "id": message.id,
        "phone": phone_number,
        "text": text
    }
    headers = {'authorization': MAILING_SERVER_TOKEN}

    response = httpx.post(f"{URL}{message.id}", json=data, headers=headers)

    if response.status_code == 400:
        raise Response400Error()
    if response.status_code == 400:
        raise BadAuthToken()

    return response.status_code, message.id


class MailingService:
    def __init__(self, mailing_instance: Mailing):
        self.mailing_instance = mailing_instance

    @staticmethod
    def set_status_mailing_by_id(mailing_id, status: Mailing.Status):
        mailing = Mailing.objects.get(pk=mailing_id)
        mailing.status = status
        mailing.save()

    @staticmethod
    def set_finish_if_all_messages_have_been_done(mailing_id):
        """Set FINISH status if all messages of this mailing have 'SENT' or 'FAILED'
        """
        unsent_messages = MessageService.get_unsent_messages_by_mailing_id(
            mailing_id=mailing_id
        )

        if not unsent_messages:
            MailingService.set_status_mailing_by_id(
                mailing_id=mailing_id,
                status=Mailing.Status.FINISHED
            )

    def start_mailing(self, **kwargs):
        clients = ClientService.get_clients(**kwargs)
        self._check_is_it_time_to_start_mailing()
        self._start_mailing(clients=clients)
        print(clients)

    def _start_mailing(self, clients):
        self.mailing_instance.status = Mailing.Status.PROCESSING
        for client in clients:
            self._send_message(
                client_id=client.id,
                phone_number=client.phone_number,
                text=self.mailing_instance.text
            )

    def _send_message(self, client_id, phone_number, text):
        send_message_task.apply_async(
            args=[client_id, phone_number, text, self.mailing_instance.id,],
            countdown=(
                (self.mailing_instance.start_at - timezone.now()).seconds
            )
        )

    def _check_is_it_time_to_start_mailing(self):
        now = timezone.now()
        if self.mailing_instance.start_at < now and \
                self.mailing_instance.end_at > now:
            return True
        return False
