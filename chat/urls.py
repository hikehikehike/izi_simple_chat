from django.urls import path, include
from rest_framework import routers

from chat.views import ThreadViewSet, MessageViewSet, MessageListCreateAPIView

router = routers.DefaultRouter()
router.register("thread", ThreadViewSet, basename="thread")
router.register("message", MessageViewSet, basename="message")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "thread/<int:pk>/messages/",
        MessageListCreateAPIView.as_view(),
        name="thread_message",
    ),
    path(
        "message/<int:pk>/mark_as_read/",
        MessageViewSet.as_view({"post": "mark_message_as_read"}),
        name="mark_message_as_read",
    ),
    path(
        "unread_message_count/",
        MessageViewSet.as_view({"get": "unread_count"}),
        name="unread_message_count",
    ),
]

app_name = "chat"
