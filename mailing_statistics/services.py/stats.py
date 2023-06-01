from django.db.models.query import Q
from core.models import Message


class MessageService:
    def __init__(self):
        pass

    @staticmethod
    def get_messages(offset=0, limit=25):
        return Message.objects.all()[offset:limit + offset]
