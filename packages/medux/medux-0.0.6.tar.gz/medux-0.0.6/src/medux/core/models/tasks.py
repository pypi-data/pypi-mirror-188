from django import apps
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from medux.core.models import Patient
from medux.common.models import BaseModel


class TaskList(models.Model):
    """This is a "continuous task list"""

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("Task List")
        verbose_name_plural = _("Task Lists")

    def __str__(self) -> str:
        return str(self.name)

    @property
    def is_complete(self) -> bool:
        return not self.tasks.filter(is_done=False).exists()

    @property
    def complete_tasks(self) -> models.QuerySet["CommonTask"]:
        return self.tasks.filter(is_done=True)

    @property
    def incomplete_tasks(self) -> models.QuerySet["CommonTask"]:
        return self.tasks.filter(is_done=False)


class CommonTask(BaseModel):
    task_list = models.ForeignKey(
        TaskList, on_delete=models.PROTECT, related_name="tasks"
    )
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Task Item")
        verbose_name_plural = _("Task Items")

    def __str__(self) -> str:
        return str(self.name)


class PatientTask(CommonTask):
    """Tasks related to a patient"""

    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, parent_link=True)


# ---------------------------------------------------------------------------
# Ideas:

# class DeviceTask(CommonTask):
#     """Tasks related to a"""
#
#     device = models.ForeignKey(Device, on_delete=models.PROTECT, parent_link=True)


# class DiagnosticReportTask(CommonTask):
#     """Tasks related to a diagnostic report.
#
#     This task is generated automatically then creating a referral to another Health care service.
#     It should be possible to keep track of it using this task.
#     Incoming diagnostic results create this Task too, so you can easily keep an eye on them."""
#
#     report = models.ForeignKey(..., on_delete=models.PROTECT, parent_link=True)
