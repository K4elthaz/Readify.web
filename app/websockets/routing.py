from django.urls import path, include, re_path
from .consumer import CollaborationConsumer, ChatConsumer

# the empty string routes to ChatConsumer, which manages the chat functionality.
websocket_urlpatterns = [
    path("ws/collaboration/<slug:slug>/", CollaborationConsumer.as_asgi()),
    path("ws/chat/<str:pk>/", ChatConsumer.as_asgi()),
]
