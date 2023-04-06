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
        return data


class ThreadListSerializer(ThreadSerializer):
    participants = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="username"
    )


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


class MessageSerializer(MessageListSerializer):
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        validated_data["sender"] = self.context["request"].user
        return super().create(validated_data)
