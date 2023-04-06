from rest_framework import viewsets

from chat.models import Thread
from chat.serializers import ThreadSerializer, MessageSerializer


class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = MessageSerializer
