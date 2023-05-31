from rest_framework import viewsets
from base import classes
from core.models import Client, Mailing
from core.serializers import (
    CreateClientSerializer,
    MailingSerializer,
    CreateMailingSerializer,
    UpdateMailingSerializer,
    ClientSerializer,
)


class MailingViewSet(classes.MixedSerializer, viewsets.ModelViewSet):
    serializer_classes_by_action = {
        'create': CreateMailingSerializer,
        'update': UpdateMailingSerializer,
        'destroy': MailingSerializer,
        'list': MailingSerializer,
        'retrieve': UpdateMailingSerializer,
        'partial_update': CreateMailingSerializer,
    }

    def get_queryset(self):
        return Mailing.objects.all()


class ClientViewSet(classes.MixedSerializer, viewsets.ModelViewSet):
    serializer_classes_by_action = {
        'create': CreateClientSerializer,
        'update': CreateClientSerializer,
        'destroy': ClientSerializer,
        'list': ClientSerializer,
        'retrieve': ClientSerializer,
        'partial_update': ClientSerializer,
    }

    def get_queryset(self):
        return Client.objects.all()
