from rest_framework import serializers

from chat.models import Thread, Message


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ("id", "participants", "created", "updated")


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "sender", "text", "thread", "created", "is_read")
