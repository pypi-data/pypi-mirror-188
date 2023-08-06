from .api import get_alerts
from django.contrib.messages.constants import DEFAULT_LEVELS


def notifications(request):
    """Return a lazy 'alerts' context variable.

    The 'DEFAULT_MESSAGE_LEVELS' is already done by django.contrib.messages."""
    return {
        "alerts": get_alerts(request),
    }
