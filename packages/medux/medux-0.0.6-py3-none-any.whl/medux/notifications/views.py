from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DeleteView

from medux import notifications
from medux.common.api.http import HttpResponseEmpty
from medux.common.htmx.mixins import HtmxResponseMixin
from medux.notifications.models import Alert


class SuccessMessageMixin:
    """
    Add a success message on successful form submission as a notification.
    """

    success_message = ""

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            notifications.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class DeleteAlertView(PermissionRequiredMixin, HtmxResponseMixin, DeleteView):
    model = Alert

    def has_permission(self):
        """Only allow deleting of own notifications"""
        return self.request.user == self.get_object().recipient

    def post(self, request, *args, **kwargs):
        self.get_object().delete()
        return HttpResponseEmpty()
