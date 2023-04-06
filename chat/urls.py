from django.urls import path, include
from rest_framework import routers

from chat.views import ThreadViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register("thread", ThreadViewSet, basename="thread")
router.register("message", MessageViewSet, basename="message")

urlpatterns = [
    path("", include(router.urls))
]

app_name = "chat"
