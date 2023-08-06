import json
import logging

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.contrib import messages
from django.db.models.signals import post_save
from django.db import models
from django.template.loader import get_template
from medux.notifications.models import Alert
from medux.notifications.signals import notify_user_from_model_instance_change
from medux.core.models import User

logger = logging.getLogger(__file__)


class AlertConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user: User = self.scope["user"]
        if self.user.is_authenticated and self.user.is_active:
            group_name = self.user.channels_group_name
            self.channel_layer.group_add(
                group_name,
                self.channel_name,
            )
            await self.accept()
            channel_layer = get_channel_layer()
            for group in self.groups:
                channel_layer.group_send(group, {"type": "message", "message": "foo"})

            # store client channel name in the user session
            self.scope["session"]["channel_name"] = self.channel_name
            self.scope["session"].save()

            # Send the initial set of messages
            # self.send_pending_messages()

    async def disconnect(self, close_code):
        # remove channel name from session
        if self.scope["user"].is_authenticated:
            if "channel_name" in self.scope["session"]:
                del self.scope["session"]["channel_name"]
                self.scope["session"].save()
            self.channel_layer.group_discard(
                self.user.channels_group_name, self.channel_name
            )

    async def websocket_receive(self, event):
        print("receive", event)

        message_type = event.get("type", None)
        if message_type == "notification":
            # Update the notification read status flag in Notification model.
            notification = Alert.objects.get(id=event.get("id"))
            notification.notification_read = True
            notification.save()  # commit to DB
            print("notification read.")

        message = event.get("message", None)
        if message is not None:
            # loaded_dict_data = json.loads(message)
            # msg = loaded_dict_data.get("message")
            # user = self.scope["user"]
            # myResponse = {
            #     "message": msg,
            #     "id": event.get("id"),
            # }
            html = get_template("common/toast.html").render(
                context={"message": event["message"]}
            )
            await self.send(text_data=html)

    # async def receive(self, text_data=None, bytes_data=None):
    #     if text_data:
    #         await self.channel_layer.group_send(
    #             self.user.channels_group_name,
    #             {"type": "notify", "message": json.loads(text_data)},
    #         )

    async def notify(self, event: dict):
        """Renders a toast message and sends the html over the wire to the client."""
        html = get_template("common/toast.html").render(
            context={"message": event["message"]}
        )
        await self.send(text_data=html)

    async def send_pending_messages(self):

        # Get the pending messages from the messages framework
        pending_messages = messages.get_messages(self.scope["user"])

        # Send the pending messages to the client
        for message in pending_messages:
            await self.send(text_data=json.dumps({"message": message.message}))

        await self.send(text_data="<div id='toasts' hx-swap-oob='True'>Hi!</div>")


class MyConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            self.close()
            return

        async_to_sync(self.channel_layer.group_add)(
            f"user-{self.user.id}",
            self.channel_name,
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            f"user-{self.user.id}",
            self.channel_name,
        )

    def notify(self, event: dict):
        html = get_template("common/toast.html").render(
            context={"message": event["message"]}
        )
        self.send(text_data=html)


class ModelConsumer(WebsocketConsumer):
    model: models.Model = None
    template_name = None
    group_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.model:
            raise AttributeError(
                f"{self.__class__.__name__} needs a 'model' attribute."
            )

    def connect(self):
        # Accept the connection
        self.group_name = self.model._meta.verbose_name
        self.accept()
        print(f"accepted connection: {self.group_name} notifications")
        # Add the client to the group for broadcast
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        print(f"Channel name: {self.channel_name}")

    def disconnect(self, code):
        # Remove the client from the group on disconnect
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        # Broadcast the new model data to all clients in the group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {"type": "model.updated", "data": json.loads(text_data)}
        )
        print(f"received text: {text_data}")

    def model_updated(self, event):
        # Send the new model data to the client
        instance = json.loads(event["data"])[0]
        html = get_template(self.template_name).render(context={**instance})
        async_to_sync(self.send)(text_data=html)
        print(f"data sent: {html}")


class NotificationConsumer(ModelConsumer):
    model = Alert
    template_name = "common/notification.html"
