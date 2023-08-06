from django import template

from medux.preferences.definitions import Scope
from medux.preferences.models import ScopedPreference
from medux.preferences.registry import PreferencesRegistry
from medux.preferences.tools import is_effective

register = template.Library()


@register.simple_tag(takes_context=True)
def effective(context, setting):
    request = context["request"]
    return is_effective(setting, request)


@register.simple_tag
def is_setting_editable(item: ScopedPreference, request) -> bool:
    # FIXME: bool is a senseless return value in a template tag

    if not PreferencesRegistry.exists(item.namespace, item.key, item.scope):
        return False
    if item.scope == Scope.TENANT:
        return False

    if (
        item.scope == Scope.USER
        and item.user == request.user
        and request.user.has_perm("preferences.change_own_user_preferences")
    ):
        return True

    if (
        item.scope == Scope.GROUP
        and item.group in request.user.groups
        and request.user.has_perm("preferences.change_group_preferences")
    ):
        return True

    if (
        item.scope == Scope.TENANT
        and item.tenant in request.user.tenant
        and request.user.has_perm("preferences.change_own_tenant_preferences")
    ):
        return True
    return False
