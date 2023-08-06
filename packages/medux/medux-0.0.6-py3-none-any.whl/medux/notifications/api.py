# this is basically a clone of django.contrib.messages which adds some functionality

from django.contrib.messages import constants

__all__ = (
    "add_alert",
    "get_alerts",
    # "get_level",
    # "set_level",
    "debug",
    "info",
    "success",
    "warning",
    "error",
    "AlertFailure",
)


class AlertFailure(Exception):
    pass


def add_alert(recipient, level, message, blocking=False, dismissible=True):
    """Add a message to the list."""
    from .models import Alert  # , Notification

    Alert.objects.create(
        level=level,
        message=message,
        recipient=recipient,
        blocking=blocking,
        dismissible=dismissible,
    )


def get_alerts(request):
    """
    Return the message storage on the request if it exists, otherwise return
    an empty list.
    """
    return getattr(request, "_alerts", [])


# def get_level(request):
#     """
#     Return the minimum level of messages to be recorded.
#
#     The default level is the ``MESSAGE_LEVEL`` setting. If this is not found,
#     use the ``INFO`` level.
#     """
#     storage = getattr(request, "_alerts", default_storage(request))
#     return storage.level
#
#
# def set_level(request, level):
#     """
#     Set the minimum level of messages to be recorded, and return ``True`` if
#     the level was recorded successfully.
#
#     If set to ``None``, use the default level (see the get_level() function).
#     """
#     if not hasattr(request, "_alerts"):
#         return False
#     request._alerts.level = level
#     return True


def debug(recipient, message, blocking=False, dismissible=True):
    """Add a message with the `DEBUG` level."""
    add_alert(recipient, constants.DEBUG, message, blocking, dismissible)


def info(recipient, message, blocking=False, dismissible=True):
    """Add a message with the `INFO` level."""
    add_alert(recipient, constants.INFO, message, blocking, dismissible)


def success(recipient, message, blocking=False, dismissible=True):
    """Add a message with the `SUCCESS` level."""
    add_alert(recipient, constants.SUCCESS, message, blocking, dismissible)


def warning(recipient, message, blocking=False, dismissible=True):
    """Add a message with the `WARNING` level."""
    add_alert(recipient, constants.WARNING, message, blocking, dismissible)


def error(message, blocking=False, dismissible=True, recipient=None):
    """Add a message with the `ERROR` level."""
    add_alert(recipient, constants.ERROR, message, blocking, dismissible)
