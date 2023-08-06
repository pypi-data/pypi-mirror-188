from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from medux.common.api.interfaces import IMenuItem
from medux.core.api import IViewMode


# class SearchViewMode(IViewMode):
#     title = _("Search")
#     url = reverse("patient_list")
#     icon = "bi-search"
#     weight = 20


# # Patient menu
# class PatientNew(IMenuItem):
#     menu = "main_menu"
#     title = _("New")
#     url = reverse("patient_new")
#     weight = 0
#     icon = "person-circle"
#
#
# class Patient(IMenuItem):
#     menu = "main_menu"
#     title = _("Patient")
#     url = "/"
#     weight = 0
#     children = [
#         PatientNew,
#         # MenuSeparator,
#     ]


class ExtrasPreferences(IMenuItem):
    title = _("Preferences")
    url = reverse("components:preferences")
    slug = "preferences"
    weight = 10
    icon = "gear"
    icon_only = True  # TODO: implement icon_only


class Extras(IMenuItem):
    menu = "main_menu"
    _("Extras")
    url = reverse("home")
    weight = 30
    children = [ExtrasPreferences]


# top right menu
class Notifications(IMenuItem):
    menu = "top_navbar"
    title = _("Notifications")
    url = reverse("home")
    weight = 20
    icon = "bi-bell"
    icon_only = True
    badge = True  # FIXME: this shouldn't be hardcoded here


# class Home(IMenuItem):
#     menu="top_navbar"
#
#     MenuItem(
#         title=lambda request: request.user,
#         url=reverse("home"),
#         slug="myaccount",
#         weight=99,
#         icon="bi-user",
#         children=[
#             MenuItem("Edit Profile", url=reverse("home"), icon="bi-user"),
#             MenuItem(
#                 title="Admin",
#                 url=reverse("admin:index"),
#                 # check=lambda request: request.user.is_superuser,
#             ),
#             MenuSeparator(),
#             MenuItem(
#                 title=_("Logout"),
#                 url=reverse("logout"),
#                 icon="bi-box-arrow-right",
#             ),
#         ],
#     ),
# )

# ------------- Views  -------------


class Search(IMenuItem):
    menu = "views"
    title = _("Search")
    url = reverse("patient_list")
    icon = "search"
    weight = 20


class File(IMenuItem):
    menu = "views"
    title = _("Patient file")
    url = "#"
    icon = "file-earmark"
    weight = 30


class Dashboard(IMenuItem):
    menu = "views"
    title = _("Dashboard")
    url = reverse("dashboard")
    icon = "gear"
    weight = 90
