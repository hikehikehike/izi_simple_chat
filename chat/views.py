from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404

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
        if "pk" in self.kwargs:
            return Message.objects.filter(thread__in=thread, id=self.kwargs["pk"])
        return Message.objects.filter(thread__in=thread)


class MessageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        thread_id = self.kwargs["pk"]
        return Message.objects.filter(thread_id=thread_id)

    def perform_create(self, serializer):
        thread_id = self.kwargs["pk"]
        thread = get_object_or_404(Thread, pk=thread_id)
        serializer.save(sender=self.request.user, thread=thread)
