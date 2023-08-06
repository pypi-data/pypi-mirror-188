from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.serializers import serialize


def notify_user_from_model_instance_change(sender, instance, **kwargs):
    """Sends the serialized data of the model to the client."""
    channel_layer = get_channel_layer()
    data = serialize("json", [instance])
    async_to_sync(channel_layer.group_send)(
        sender._meta.verbose_name,
        {"type": "model.updated", "data": data},
    )
    print("model.updated sent:", data)  # FIXME delete line
