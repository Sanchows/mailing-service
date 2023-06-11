from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from base import classes
from core.models import Client, Mailing
from core.serializers import (ClientSerializer, CreateClientSerializer,
                              CreateMailingSerializer, MailingSerializer,
                              UpdateMailingSerializer)


@extend_schema(tags=["Mailings"])
@extend_schema_view(
    retrieve=extend_schema(
        summary="Получить рассылку",
        description="Получить рассылку по id",
    ),
    list=extend_schema(
        summary="Получить список рассылок",
        description="Получить список всех рассылок",
    ),
    update=extend_schema(
        summary="Изменение существующей рассылки",
        description="Изменение существующей рассылки по ID",
    ),
    partial_update=extend_schema(
        summary="Частичное изменение существующей рассылки",
        description="Частичное изменение существующей рассылки по ID",
    ),
    create=extend_schema(
        summary="Создание новой рассылки",
        description="Создание новой рассылки",
    ),
    destroy=extend_schema(
        summary="Удаление рассылки",
        description="Удаление рассылки",
    ),
)
class MailingViewSet(classes.MixedSerializer, viewsets.ModelViewSet):
    serializer_classes_by_action = {
        'create': CreateMailingSerializer,
        'update': UpdateMailingSerializer,
        'destroy': MailingSerializer,
        'list': MailingSerializer,
        'retrieve': MailingSerializer,
        'partial_update': UpdateMailingSerializer,
    }

    def get_queryset(self):
        return Mailing.objects.all()


@extend_schema(tags=["Clients"])
@extend_schema_view(
    retrieve=extend_schema(
        summary="Получить клиента",
        description="Получить клиента по ID",
    ),
    list=extend_schema(
        summary="Получить список клиентов",
        description="Получить список всех клиентов",
    ),
    update=extend_schema(
        summary="Изменение существующего клиента",
        description="Изменение существующего клиента",
    ),
    partial_update=extend_schema(
        summary="Частичное изменение существующего клиента",
        description="Частичное изменение существующего клиента",
    ),
    create=extend_schema(
        summary="Создание нового клиента",
        description="Создание нового клиента",
    ),
    destroy=extend_schema(
        summary="Удалить клиента",
        description="Удалить клиента",
    ),
)
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
