from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return ThreadListSerializer
        return ThreadSerializer


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return MessageListSerializer
        return MessageSerializer

    def get_queryset(self):
        thread = Thread.objects.filter(participants=self.request.user)
        if "pk" in self.kwargs:
            queryset = Message.objects.select_related("thread", "sender").filter(
                thread__in=thread, id=self.kwargs["pk"]
            )
        else:
            queryset = Message.objects.select_related("thread", "sender").filter(
                thread__in=thread
            )
        return queryset

    @action(detail=True, methods=["post"])
    def mark_message_as_read(self, request, pk=None):
        message = self.get_object()
        message.is_read = True
        message.save()
        return Response({"message": "Message updated successfully."})

    @action(detail=False, methods=["get"])
    def unread_count(self, request):
        user = request.user
        unread_count = Message.objects.filter(sender=user, is_read=False).count()
        return Response({"unread_count": unread_count})


class MessageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        thread_id = self.kwargs["pk"]
        return Message.objects.select_related("thread", "sender").filter(
            thread_id=thread_id
        )

    def perform_create(self, serializer):
        thread_id = self.kwargs["pk"]
        thread = get_object_or_404(Thread, pk=thread_id)
        serializer.save(sender=self.request.user, thread=thread)
