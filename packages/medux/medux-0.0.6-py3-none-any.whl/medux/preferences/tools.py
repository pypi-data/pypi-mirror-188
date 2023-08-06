# no global imports of models,
# so this functions can be used before apps are loaded.
from typing import Any

from django.http import HttpRequest

PreferencesContext = dict[str, Any]


def is_editable(setting, request: HttpRequest):
    from medux.preferences.definitions import Scope

    match setting.scope:
        case Scope.VENDOR:
            return False
        case Scope.TENANT:
            return (
                request.user.has_perm("preferences.change_own_tenant_scopedpreference")
                and setting.tenant == request.user.tenant
            )
        case Scope.USER:
            return request.user.has_perm("preferences.change_own_user_scopedpreference")
        case Scope.GROUP:
            return (
                request.user.has_perm("preferences.change_own_group_scopedpreference")
                and setting.group in request.user.groups.all()
            )
        case Scope.DEVICE:
            return request.user.has_perm("preferences.change_device_scopedpreference")


def is_deletable(setting, request: HttpRequest):
    return is_editable(setting, request)


def is_effective(setting, request: HttpRequest):
    return setting == get_effective_setting(setting.namespace, setting.key, request)


def get_effective_setting(namespace: str, key: str, request):
    """
    :return: the effective ScopedPreference with the give namespace/key.
    """
    from .models import ScopedPreference
    from medux.preferences.definitions import Scope

    queryset = ScopedPreference.objects.filter(
        base__namespace=namespace, base__key=key
    ).order_by("-scope")

    # traverse preferences in reverse Order (USER -> VENDOR),
    # and take the first matching
    for item in queryset:
        scope = item.scope

        if scope == Scope.USER and request.user == item.user:
            return item

        if scope == Scope.DEVICE and request.device == item.device:
            return item

        if scope == Scope.GROUP and item.group in request.user.groups.all():
            return item

        if scope == Scope.TENANT:
            # for authenticated users, the user's tenant counts!
            if request.user.is_authenticated:
                if request.user.tenant == item.tenant:
                    return item
            # for anonymous users, the site tenant is the valid one.
            else:
                if request.site.tenant == item.tenant:
                    return item

        if scope == Scope.VENDOR:
            return item
