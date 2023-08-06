from medux.notifications.models import Alert


class AlertMiddleware:
    """Middleware that handles notifications and alerts."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # get alerts for authenticated user
            request._alerts = Alert.objects.filter(recipient=request.user)
        else:
            # get alerts for all/anonymous users
            request._alerts = Alert.objects.filter(recipient=None)
        response = self.get_response(request)
        return response
