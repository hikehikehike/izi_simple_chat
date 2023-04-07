from django.core.exceptions import ValidationError
from rest_framework import serializers

from chat.models import Thread, Message


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = (
            "id",
            "participants",
            "created",
            "updated",
        )
        read_only_fields = (
            "created",
            "updated",
        )

    def validate(self, data):
        if len(data["participants"]) != 2:
            raise ValidationError("Thread must have exactly 2 participants.")
        if self.context["request"].user not in data["participants"]:
            raise serializers.ValidationError(
                "You should choose yourself to create a thread"
            )
        return data


class ThreadListSerializer(ThreadSerializer):
    participants = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="username"
    )
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = (
            "id",
            "participants",
            "created",
            "updated",
            "last_message",
        )

    @staticmethod
    def get_last_message(obj):
        last_message = obj.messages.order_by("-created").first()
        if last_message:
            return {
                "id": last_message.id,
                "sender": last_message.sender.username,
                "text": last_message.text,
                "created": last_message.created,
                "is_read": last_message.is_read,
            }
        return None


class MessageListSerializer(serializers.ModelSerializer):
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
            "created",
            "is_read",
        )
        read_only_fields = ("is_read",)


class MessageSerializer(MessageListSerializer):
    def create(self, validated_data):
        validated_data["sender"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        thread = data.get("thread")
        participants = thread.participants.all()

        if self.context["request"].user not in participants:
            raise serializers.ValidationError(
                "You cannot send messages to threads in which you are not a participant."
            )

        return data
