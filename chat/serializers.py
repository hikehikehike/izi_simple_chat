from django.core.exceptions import ValidationError
from rest_framework import serializers

from chat.models import Thread, Message


class ThreadSerializer(serializers.ModelSerializer):
    """
    Serializer for the Thread model.
    """

    class Meta:
        model = Thread
        fields = (
            "id",
            "participants",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "created_at",
            "updated_at",
        )

    def validate(self, data):
        """
        Validate that the Thread has exactly 2 participants
        and that the current user is one of them.
        """
        if len(data["participants"]) != 2:
            raise ValidationError("Thread must have exactly 2 participants.")
        if self.context["request"].user not in data["participants"]:
            raise serializers.ValidationError(
                "You should choose yourself to create a thread"
            )
        return data


class ThreadListSerializer(ThreadSerializer):
    """
    Serializer for a list of Threads.
    """

    participants = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="username"
    )
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = (
            "id",
            "participants",
            "created_at",
            "updated_at",
            "last_message",
        )

    @staticmethod
    def get_last_message(obj):
        """
        Get the last message in the Thread.
        """
        last_message = obj.messages.order_by("-created_at").first()
        if last_message:
            return {
                "id": last_message.id,
                "sender": last_message.sender.username,
                "text": last_message.text,
                "created_at": last_message.created_at,
                "is_read": last_message.is_read,
            }
        return None


class MessageListSerializer(serializers.ModelSerializer):
    """
    Serializer for a list of Messages.
    """

    sender = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="username"
    )

    class Meta:
        model = Message
        fields = (
            "id",
            "sender",
            "text",
            "thread",
            "created_at",
            "is_read",
        )
        read_only_fields = ("is_read",)


class MessageSerializer(MessageListSerializer):
    """
    Serializer for the Message model.
    """

    def create(self, validated_data):
        """
        Create a new Message object and set the sender to the current user.
        """
        validated_data["sender"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """
        Validate that the current user is a participant in the Thread that the Message belongs to.
        """
        thread = data.get("thread")
        participants = thread.participants.all()

        if self.context["request"].user not in participants:
            raise serializers.ValidationError(
                "You cannot send messages to threads in which you are not a participant."
            )

        return data
