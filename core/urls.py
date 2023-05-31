from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import MailingViewSet, ClientViewSet

api_router = DefaultRouter()
api_router.register('mailing', MailingViewSet, basename='mailing')
api_router.register('client', ClientViewSet, basename='client')

urlpatterns = [
    path('', include(api_router.urls)),
]
