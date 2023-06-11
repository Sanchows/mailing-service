from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, viewsets

from base.pagination import PageNumberPagination
from core.models import Message
from mailing_statistics.serializers import (
    MessageClientByStatusSerializer,
    MessageSerializer,
)


@extend_schema(tags=["Messages"])
@extend_schema_view(
    retrieve=extend_schema(
        summary="Получить сообщение",
        description="Получить сообщение по ID",
    ),
    list=extend_schema(
        summary="Получить список всех сообщений",
        description="Получить список всех сообщений",
    ),
)
class MessageView(generics.ListAPIView,
                  generics.RetrieveAPIView,
                  viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    serializer_class = MessageSerializer
    queryset = Message.objects.all()


@extend_schema(tags=["Messages"],)
@extend_schema_view(
    list=extend_schema(
        operation_id="ClientMessagesByClientId",
        summary="Получить список всех сообщений клиента по ID клиента",
        description="Получить список всех сообщений клиента по ID клиента",
    ),
)
class MessagesClientView(generics.ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    lookup_field = 'client__id'

    @extend_schema(
        operation_id="ClientMessagesByClientId",
        summary="Получить список всех сообщений клиента по ID клиента",
        description="Получить список всех сообщений клиента по ID клиента",
    )
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


@extend_schema(tags=["Messages"])
class MessagesClientByStatusView(generics.ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = MessageClientByStatusSerializer

    @extend_schema(
        operation_id="ClientMessagesByClientIdAndStatus",
        summary="""Получить список всех сообщений определенного
                   статуса по ID клиента""",
        description="""Получить список всех сообщений клиента
                    по ID клиента и статусу сообщения""",)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_queryset(self):
        client_id = self.kwargs['client_id']
        status = self.kwargs['message_status']
        queryset = Message.objects.filter(
            client_id=client_id,
            status=status
        )
        return queryset
