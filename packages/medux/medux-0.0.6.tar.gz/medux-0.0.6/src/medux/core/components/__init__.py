from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from medux.core.api import IDashboardSection


class PreferencesComponent(IDashboardSection, TemplateView):
    template_name = "core/dashboard/preferences.html"
    name = "preferences"
    title = _("Preferences")
    icon = "gear"
    weight = 100
