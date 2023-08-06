from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from medux.employees.models import (
    WorkingContract,
    WorkingTimeRange,
    Application,
    Classification,
    WorkSchedule,
    Employee,
)


class WorkingHourRangeInline(admin.StackedInline):
    model = WorkingTimeRange
    extra = 5


@admin.register(WorkingContract)
class Contract(admin.ModelAdmin):
    pass


@admin.register(WorkSchedule)
class SetAdmin(admin.ModelAdmin):
    inlines = [WorkingHourRangeInline]


admin.site.register(WorkingTimeRange)
admin.site.register(Classification)
admin.site.register(Application)


class EmployeeAdmin(UserAdmin):
    model = Employee
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (None, {"fields": ("tenant", "color")}),
        (None, {"fields": ("active_work_schedule",)}),  # added
    )


admin.site.register(Employee, EmployeeAdmin)
