from rest_framework import viewsets

from chat.models import Thread, Message
from chat.serializers import (
    ThreadSerializer,
    MessageSerializer,
    MessageListSerializer,
    ThreadListSerializer,
)


class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ThreadListSerializer
        return ThreadSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return MessageListSerializer
        return MessageSerializer

    def get_queryset(self):
        thread = Thread.objects.filter(participants=self.request.user)
        return Message.objects.filter(thread__in=thread)
