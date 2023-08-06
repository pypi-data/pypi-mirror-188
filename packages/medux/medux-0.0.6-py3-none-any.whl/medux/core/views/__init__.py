# from django.contrib.auth import get_user_model
# User = get_user_model()
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import TemplateView, DetailView

from medux.common.api.interfaces import UseComponentMixin
from medux.core.api import IViewMode, IGlobalJavascript, IDashboardSection
from medux.core.models import Patient


class MeduxBaseMixin(PermissionRequiredMixin):
    """Mixin for all views that MedUX uses.

    Inherit from this view if you want to create a new page etc. in MedUX.
    You have to specify the `permission_required` attribute or `has_permission`
    method, since all MedUX views need to have a valid permission for seeing it.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "viewmodes": iter(IViewMode),
                "global_javascripts": iter(IGlobalJavascript),
            }
        )
        return context


class HomeView(MeduxBaseMixin, TemplateView):
    template_name = "home.html"
    # FIXME find a correct permission for home, and use MeduxBaseMixin
    extra_context = {
        "viewmodes": iter(IViewMode),
    }

    def has_permission(self):
        return self.request.user.is_authenticated


class PatientFileView(MeduxBaseMixin, DetailView):
    model = Patient
    context_object_name = "patient"
    permission_required = "can view user"
    template_name = "core/patient_file_detail.html"


class DashboardView(UseComponentMixin, LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"
    components = [IDashboardSection]
