from rest_framework import generics, mixins, viewsets
from rest_framework.response import Response

from base.pagination import PageNumberPagination
from core.models import Message
from mailing_statistics.serializers import StatisticsMessageSerializer


class MessagesView(generics.ListAPIView, generics.RetrieveAPIView, viewsets.GenericViewSet):
    """
    View to list all messages in the system.
    """
    pagination_class = PageNumberPagination
    serializer_class = StatisticsMessageSerializer
    queryset = Message.objects.all()


class MessagesGroupView(generics.ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = StatisticsMessageSerializer
    queryset = Message.objects.all()
    lookup_field = 'client__id'
