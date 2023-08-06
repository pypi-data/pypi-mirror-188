from datetime import timedelta

from dateutil.utils import today
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.timezone import now

from .models import (
    WorkingContract,
    WorkingTimeRange,
    DaysOfWeek,
    Classification,
    Application,
    WorkSchedule,
    Employee,
)
from ..common.models import Tenant

User = get_user_model()


class WorkScheduleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.employee = Employee.objects.create_user("tom", id=1)
        cls.work_schedule = WorkSchedule.objects.create(
            id=1,
            start_date=now() - timedelta(days=100),
            user=cls.employee,  # end_date=now(),
        )

    def setUp(self):
        self.whr1 = WorkingTimeRange.objects.create(
            weekday=DaysOfWeek.MONDAY,
            start_time="08:00",
            end_time="12:00",
            work_schedule=self.work_schedule,
        )
        self.whr2 = WorkingTimeRange.objects.create(
            weekday=DaysOfWeek.MONDAY,
            start_time="13:00",
            end_time="17:00",
            work_schedule=self.work_schedule,
        )
        self.whr3 = WorkingTimeRange.objects.create(
            weekday=DaysOfWeek.TUESDAY,
            start_time="08:00",
            end_time="17:00",
            work_schedule=self.work_schedule,
        )

    def test_total_working_hours(self):
        self.assertEqual(self.work_schedule.total_working_hours(), timedelta(hours=17))


class WorkingContractTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.classification1 = Classification.objects.create(id=1, name="Nurse")
        cls.application1 = Application.objects.create(id=1, name="Worker")
        cls.tenant1 = Tenant.objects.create(
            id=1,
            first_name="John",
            last_name="Doe",
            sex="male",
            address="Nowhere",
        )
        cls.employee = Employee.objects.create_user("tom", id=1)
        cls.work_schedule = WorkSchedule.objects.create(
            id=1,
            start_date=now() - timedelta(days=100),
            user=cls.employee,  # end_date=now(),
        )

    def setUp(self):
        self.contract = WorkingContract.objects.create(
            start_date=today(),
            salary=500.0,
            holidays=25,
            special_holidays=10,
            classification_id=1,
            intended_application_id=1,
            tenant_id=1,
            employee_id=1,
            initial_work_schedule=self.work_schedule,
        )

    # def test_foo(self):
