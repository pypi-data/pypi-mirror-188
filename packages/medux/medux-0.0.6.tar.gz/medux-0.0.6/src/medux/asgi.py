"""
ASGI config for medux project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from medux.notifications import consumers

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "medux.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    path("ws/messages", consumers.MyConsumer.as_asgi()),
                    path("ws/notifications", consumers.NotificationConsumer.as_asgi()),
                ]
            )
        ),
    }
)
