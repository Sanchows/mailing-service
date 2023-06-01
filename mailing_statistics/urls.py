from django.urls import include, path
from rest_framework.routers import DefaultRouter

from mailing_statistics.views import (
    MessagesView, MessagesClientView, MessagesClientByStatusView
)


api_router = DefaultRouter()
api_router.register('message', MessagesView, basename='message')

urlpatterns = [
    path('',
         include(api_router.urls)),
    path('message/client/<uuid:client_id>',
         MessagesClientView.as_view(),
         name='client-messages'),
    path('message/client/<uuid:client_id>/<str:message_status>',
         MessagesClientByStatusView.as_view(),
         name='client-messages-by-id'),

]
