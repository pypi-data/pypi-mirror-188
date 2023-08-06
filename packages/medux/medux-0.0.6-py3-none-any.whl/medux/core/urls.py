from django.contrib.auth.views import LogoutView, PasswordResetView
from django.urls import path, include
from gdaps.pluginmanager import PluginManager

from . import views
from .views import HomeView, PatientFileView
from .views.patient_file import NewPatientView, PatientListView
from medux.common.api.interfaces import IHTMXComponentMixin
from medux.common.views import LoginView

app_name = "core"
# components must be loaded before assigning their urlpaths
PluginManager.load_plugin_submodule("components")

root_urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(
        "__components__/",
        include(
            (IHTMXComponentMixin.get_url_patterns(), "components"),
            namespace="components",
        ),
    ),
    path("patient/", PatientListView.as_view(), name="patient_list"),
    path("patient/file/<pk>", PatientFileView.as_view(), name="patient_file"),
    path("patient/add/", NewPatientView.as_view(), name="patient_new"),
    # path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    path(
        "accounts/password-reset/", PasswordResetView.as_view(), name="password_reset"
    ),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("notifications/", include("medux.notifications.urls"), name="notifications"),
]

# Django login accounts views:
# accounts/login/ [name='login']
# accounts/logout/ [name='logout']
# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']
