from django.conf import settings
from django.contrib import messages
from django.template import Context
from gdaps.api import Interface
from gdaps.api.interfaces import ITemplatePluginMixin

from medux.common.api.interfaces import IHTMXComponentMixin


@Interface
class IViewMode:
    """Interface for MedUX ViewModes.

    A ViewMode provides data and methods for displaying an icon for the
    main viewing modes of MedUX.
    """

    __service__ = True

    title = ""
    """The title which is displayed when hovering over the icon."""

    url = ""
    """the URL that should be called. Can be a Dajngo reverse() URL."""

    icon = "bi-file-earmark"
    """the icon as text, using Bootstrap Icons"""

    icon_type = "bi"  # png
    """icon_type determines where the icon is fetched from:
        bi (Bootstrap icon) or png, then it is loaded from static files"""

    weight = 0
    """the weight of the icon in the list. The higher the weight, the "deeper" the icon."""


@Interface
class IGlobalJavascript:
    """Interface for adding Js file to a global scope.

    The given file will be loaded in the global context and is then available to
    all other plugins too, in every loaded page.
    Be aware just to add Js code that is small and fast, to not blow up the application
    as whole.

    You have to specify the (relative to static dir) file path of the Js script in the
    `file` attribute.
    """

    __service__ = True

    file: str = ""
    """The (relative to static dir) file path of the Js script"""


@Interface
class ICommand:
    """A CommandLine command that executes a defined function on a shortcut.

    A written command could be ``m dicl 75`` what means the "m" command with could be parsed
    as "medication" command with a search for "Diclofenac 75mg Tbl"."""

    shortcut: str = None
    description: str = None

    def execute(self, *args, **kwargs):
        raise NotImplementedError


@Interface
class IDashboardSection(IHTMXComponentMixin):
    def has_permission(self):
        return self.request.user.is_authenticated
