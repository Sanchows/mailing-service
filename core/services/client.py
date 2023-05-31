from django.db.models.query import Q
from core.models import Client


class ClientService:
    def __init__(self):
        pass

    @staticmethod
    def get_clients(**kwargs):
        return Client.objects.filter(
            Q(code__in=kwargs['codes']) &
            Q(tags__in=kwargs['tags'])
        )
