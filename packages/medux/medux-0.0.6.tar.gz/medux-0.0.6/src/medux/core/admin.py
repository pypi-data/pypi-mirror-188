from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .forms import DosageForm
from .models import (
    Name,
    Address,
    Country,
    ContactPoint,
    AdministrativeGender,
    HealthServiceProvider,
    Physician,
    Hospital,
    Person,
    Patient,
    Encounter,
    Problem,
    Narrative,
    NarrativeType,
    Department,
    Specialty,
    Language,
    Dosage,
)

admin.site.site_header = _("MedUX administration")
admin.site.index_title = "Model administration"


class MeduxAdmin(admin.ModelAdmin):
    """A ModelAdmin for MeduxModels with Softdeletion awareness"""

    def get_queryset(self, request):
        # use the all_objects manager
        qs = self.model.all_objects

        # The below is copied from the base implementation in BaseModelAdmin to
        # prevent other changes in behavior
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def delete_model(self, request, obj):
        obj.hard_delete()


@admin.register(AdministrativeGender)
class AdministrativeGenderAdmin(admin.ModelAdmin):
    ordering = ("sort_weight",)


@admin.register(Dosage)
class DosageAdmin(admin.ModelAdmin):
    form = DosageForm
    fields = [
        "method",
        "dose_type",
        "dose_rate_numerator_value",
        "dose_rate_numerator_unit",
    ]


for model in [
    Country,
    ContactPoint,
    Address,
    # Period,
    HealthServiceProvider,
    Physician,
    Specialty,
    Hospital,
    Person,
    Patient,
    Encounter,
    Problem,
    Narrative,
    NarrativeType,
    Name,
    Department,
    Language,
]:
    admin.site.register(model)


# if settings.DEBUG:
#     # all other models
#     models = apps.get_models()
#
#     for model in models:
#         try:
#             if not model._meta.abstract:
#                 admin.site.register(model)
#         except admin.sites.AlreadyRegistered:
#             pass
