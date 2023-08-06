from django.conf import settings
from django.contrib import messages
from django.db import models
from django.db.models import IntegerChoices
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class MessageTags(IntegerChoices):
    SUCCESS = messages.SUCCESS, "success"
    DEBUG = messages.DEBUG, "info"
    INFO = messages.INFO, "info"
    WARNING = messages.WARNING, "warning"
    ERROR = messages.ERROR, "danger"


class AbstractNotification(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(editable=False, default=timezone.now)
    level = models.PositiveIntegerField(
        choices=MessageTags.choices, default=messages.INFO
    )
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=1024)

    def tags(self):
        """return MESSAGE_TAGS based on level for this Notification, to be used in templates as classes."""
        return settings.MESSAGE_TAGS[self.level]


# class Notification(AbstractNotification):
#     """A Notification to one user with variable content"""


class Alert(AbstractNotification):
    """A blocking or non-blocking, optionally dismissible notification for one user."""

    blocking = models.BooleanField(
        default=False, help_text=_("Should the alert block the user's workflow?")
    )
    dismissible = models.BooleanField(
        default=True,
        help_text=_(
            "Should the notification be dismissible by the "
            "user? If not, it will fade away itself."
        ),
    )

    def __str__(self):
        return self.message
