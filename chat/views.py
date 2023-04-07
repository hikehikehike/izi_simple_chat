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
    """
    API endpoint that allows threads to be viewed or edited.
    """

    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return ThreadListSerializer
        return ThreadSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """

    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return MessageListSerializer
        return MessageSerializer

    def get_queryset(self):
        """
        Returns the list of messages for the current user and the given thread.
        If "pk" is present in kwargs, returns a specific message with that id.
        """
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
        """
        Marks a specific message as read.
        """
        message = self.get_object()
        message.is_read = True
        message.save()
        return Response({"message": "Message updated successfully."})

    @action(detail=False, methods=["get"])
    def unread_count(self, request):
        """
        Returns the count of unread messages for the current user.
        """
        user = request.user
        unread_count = Message.objects.filter(sender=user, is_read=False).count()
        return Response({"unread_count": unread_count})


class MessageListCreateAPIView(generics.ListCreateAPIView):
    """
    API endpoint that allows messages to be listed or created for a specific thread.
    """

    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns the list of messages for the given thread.
        """
        thread_id = self.kwargs["pk"]
        return Message.objects.select_related("thread", "sender").filter(
            thread_id=thread_id
        )

    def perform_create(self, serializer):
        """
        Saves the created message with the current user as the sender and the given thread.
        """
        thread_id = self.kwargs["pk"]
        thread = get_object_or_404(Thread, pk=thread_id)
        serializer.save(sender=self.request.user, thread=thread)
