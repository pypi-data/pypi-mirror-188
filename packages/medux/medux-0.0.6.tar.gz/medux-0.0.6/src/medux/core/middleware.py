import logging

logger = logging.getLogger(__file__)


class DeviceMiddleware:
    """A middleware that adds the current device to the request.

    A device commonly is a computer in this context.
    Add ``medux.common.middleware.DeviceMiddleware`` to your MIDDLEWARE
    dict in settings.py.
    You can use the device in a template to your needs:

    .. code:: django

        <span>Device: {{ request.device }}</span>

    Or in a view:

    .. code:: python

        logger.debug(f"Request originating from device {request.device}.")
    """

    def __init__(self, get_response):
        """Initializes the middleware"""
        self.get_response = get_response

    def __call__(self, request):
        # TODO: implement device fetching in middleware
        request.device = None
        response = self.get_response(request)
        # logger.debug(f"Current device: {request.site.tenantsite}.")
        return response
