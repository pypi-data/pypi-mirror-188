import calendar
from datetime import timedelta

import typing
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum, F
from django.utils import timezone
from django.utils.formats import date_format, time_format
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField

from medux.common.constants import DaysOfWeek
from medux.common.models import BaseModel, Tenant, CreatedModifiedModel

User = get_user_model()


class Classification(models.Model):
    """The classification in an employment context.

    This could be "doctor", "nurse", etc.
    """

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("Classification")
        verbose_name_plural = _("Classifications")


class Application(models.Model):
    """The "usage field" of an employee.

    Could be "medical assistent"
    """

    name = models.CharField(max_length=255)


class WorkSchedule(CreatedModifiedModel):
    """A set of working hour ranges, for one user / one week.

    E.g. Mon 8-12, Tue 8-12, Wed-Fr 9-11

    Note:
        [WorkingTimeRange] has a ForeignKey to this class, so you can access them
        using `self.working_hours`.

    """

    employee = models.ForeignKey(
        "Employee", on_delete=models.CASCADE, related_name="work_schedules"
    )
    start_date = models.DateField(_("Start date"), default=timezone.localdate)
    end_date = models.DateField(_("End date"), blank=True, null=True)

    def total_working_hours(self):
        total_hours = self.working_hours.all().aggregate(
            total=Sum(F("end_time") - F("start_time"))
        )
        return total_hours["total"]

    def __str__(self):
        # a = [str(wa) for wa in self.working_hours.all().order_by("weekday")]
        # return f"{self.employee}: {', '.join(a)}"
        return f"{self.employee}: {date_format(self.start_date,'SHORT_DATE_FORMAT')}"

    @classmethod
    def get_active(cls, employee) -> typing.Union["WorkSchedule", None]:
        """Returns "active" work schedule, which is the one that has no end date."""
        # there *has* to be only one per user with no end date.
        try:
            return cls.objects.get(employee=employee, end_date=None)
        except cls.DoesNotExist:
            return None

    def save(self, **kwargs):
        # end last WorkSchedule with day before this one starts.
        last = self.get_active(self.employee)
        if last:
            last.end_date = self.start_date - timedelta(days=1)
        super().save(**kwargs)


class Employee(User):
    """Proxy model for user to encapsulate employment functions."""

    active_work_schedule = models.ForeignKey(
        WorkSchedule, on_delete=models.PROTECT, blank=True, null=True, related_name="+"
    )


class WorkingContract(BaseModel):
    """A contract a user has with his employer.

    Working hours, salary, and other details should be fixed within a contract,
    for a given period.
    """

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    start_date = models.DateField(_("Start date"))
    end_date = models.DateField(_("End date"), blank=True, null=True)
    notice_period_weeks = models.PositiveIntegerField(
        _("Notice period in weeks"), blank=True, null=True
    )
    notice_period_months = models.PositiveIntegerField(
        _("Notice period in months"), blank=True, null=True
    )
    # location = models.ForeignKey(Practice)
    classification = models.ForeignKey(Classification, on_delete=models.PROTECT)
    intended_application = models.ForeignKey(Application, on_delete=models.PROTECT)
    salary = MoneyField(max_digits=14, decimal_places=2, default_currency="EUR")
    salary_notice = models.TextField(
        _("Additional notice for salary"), blank=True, null=True
    )
    holidays = models.PositiveIntegerField(
        _("Holidays (days/year)"), blank=True, null=True
    )
    special_holidays = models.PositiveIntegerField(
        _("Special holidays (days/year)"), blank=True, null=True
    )
    initial_work_schedule = models.ForeignKey(
        WorkSchedule,
        on_delete=models.PROTECT,
        verbose_name=_("Regular working hours per week"),
    )


class WorkingTimeRange(models.Model):
    """A working hours range blueprint

    This is meant generically, e.g. for each Monday 8:00-15:00.
    There can be more than one WorkingTimeRange objects for one weekday, e.g.
    an employee could work on Tuesdays from 8-11 and 16-19.

    For real "worked" hours, use [TimeEntry] from the timetracker plugin.
    """

    weekday = models.PositiveSmallIntegerField(
        _("Week day"), choices=DaysOfWeek.choices
    )
    start_time = models.TimeField(_("Start time"))
    end_time = models.TimeField(_("End time"))
    work_schedule = models.ForeignKey(
        WorkSchedule, on_delete=models.CASCADE, related_name="working_hours"
    )

    def __str__(self):
        return (
            f"{_(calendar.day_abbr[self.weekday])} "
            f"{time_format(self.start_time)}-"
            f"{time_format(self.end_time)}"
        )

    def duration(self) -> timedelta:
        return timedelta(
            hours=self.end_time.hour - self.start_time.hour,
            minutes=self.end_time.minute - self.start_time.minute,
        )

    def duration_h(self) -> float:
        return self.duration().seconds / 60 / 60

    def weekday_str(self) -> str:
        return _(calendar.day_name[self.weekday])

    # @classmethod
    # def get_active(cls, thetime: datetime = None):
    #     """Get the WTR (WorkingTimeRange) that fits to the given time.
    #
    #     1. If the time is exactly within a WTR, take that. If not,
    #     2. if there is a WTR that is coming next, take that. This is if you e.g. log
    #         in a few minutes before working starts. If nothing found, then
    #     3. if there is a WTR that lies in the past and is already finished, take that.
    #     4. If nothing ws found, return None.
    #
    #     Attributes:
    #         thetime: the time to look for. If None, take the current time.
    #     """
    #     if not thetime:
    #         thetime = timezone.now()
    #
    #     weekday: int = thetime.weekday()
    #     thetime: datetime.time = thetime.time()
    #
    #     # get the first block that has already started and is not finished yet.
    #     # this is the default assumption
    #     active_block = (
    #         cls.objects.filter(start__lte=thetime, end__gt=thetime)
    #         .order_by("-start")
    #         .first()
    #     )
    #
    #     if not active_block:
    #         next_block = cls.objects.filter(start__gt=thetime).order_by("start").first()
    #         prev_block = cls.objects.filter(end__lte=thetime).order_by("-end").first()
    #         if next_block and prev_block:
    #             if (thetime - prev_block.end).total_seconds() < (
    #                 next_block.start - thetime
    #             ).total_seconds():
    #                 active_block = prev_block
    #             else:
    #                 active_block = next_block
    #         elif next_block:
    #             # there is only a next block, no previous
    #             active_block = next_block
    #         else:
    #             # there is only a previous block, and no next one.
    #             active_block = prev_block
    #         return active_block
    #
    #     active_block = (
    #         cls.objects.filter(start__lte=thetime, end__gt=thetime)
    #         .order_by("-start")
    #         .first()
    #     )
    #     if not active_block:
    #         # if no block has already started, take the next available.
    #         active_block = (
    #             cls.objects.filter(start__gt=thetime).order_by("start").first()
    #         )
    #
    #     if not active_block:
    #         # if there is no block in the future, take the last one, even if it is already in the past
    #         active_block = (
    #             cls.objects.filter(start__lte=thetime).order_by("-start").first()
    #         )
    #
    #     return active_block
