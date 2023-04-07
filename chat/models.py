from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model with created_at and updated_at timestamps.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Thread(BaseModel):
    """
    Thread model representing a conversation between two participants.
    """

    participants = models.ManyToManyField("user.User", related_name="threads")

    class Meta:
        ordering = ["-updated_at"]


class Message(BaseModel):
    """
    Message model representing a message sent by a user in a thread.
    """

    sender = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="sender"
    )
    text = models.TextField()
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name="messages"
    )
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
