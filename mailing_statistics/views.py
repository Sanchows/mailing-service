from rest_framework import generics, viewsets

from base.pagination import PageNumberPagination
from core.models import Message
from mailing_statistics.serializers import (
    MessageSerializer, MessageClientByStatusSerializer,
)


class MessageView(generics.ListAPIView,
                  generics.RetrieveAPIView,
                  viewsets.GenericViewSet):
    """
    View to list all messages in the system.
    """
    pagination_class = PageNumberPagination
    serializer_class = MessageSerializer
    queryset = Message.objects.all()


class MessagesClientView(generics.ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    lookup_field = 'client__id'


class MessagesClientByStatusView(generics.ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = MessageClientByStatusSerializer

    def get_queryset(self):
        client_id = self.kwargs['client_id']
        status = self.kwargs['message_status']
        queryset = Message.objects.filter(
            client_id=client_id,
            status=status
        )
        return queryset
