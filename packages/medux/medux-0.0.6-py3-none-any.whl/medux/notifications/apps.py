from django.apps import AppConfig
from django.db.models.signals import post_save

# from django.contrib.messages.storage import base
# from django.contrib.messages.utils import get_level_tags
# from django.core.signals import setting_changed
from django.utils.translation import gettext_lazy as _


# def update_level_tags(setting, **kwargs):
#     if setting == "MESSAGE_TAGS":
#         base.LEVEL_TAGS = get_level_tags()


class NotificationsConfig(AppConfig):
    name = "medux.notifications"
    verbose_name = _("Notifications")

    def ready(self):
        from . import signals
        from ..notifications.models import Alert

        post_save.connect(signals.notify_user_from_model_instance_change, sender=Alert)

    #     setting_changed.connect(update_level_tags)
