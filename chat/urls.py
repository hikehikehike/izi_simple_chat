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
]

app_name = "chat"
