import calendar
from datetime import time, datetime
from io import BytesIO
from logging import getLogger
from pathlib import Path

from django.core.files import File
from django.db.models import Model  # FIXME could be a problem during migrations
from PIL import Image

logger = getLogger(__file__)


def create_groups_permissions(
    groups_permissions: dict[str, dict[Model | str, list[str]]]
):
    """Creates groups and their permissions defined in given `groups_permissions` automatically.

    Attributes:
         groups_permissions: a dict, see also [MeduxPluginAppConfig.groups_permissions]


    """
    # Based upon the work here: https://newbedev.com/programmatically-create-a-django-group-with-permissions
    from django.apps import apps
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType

    for group_name in groups_permissions:

        # Get or create group (even if there are no permissions
        # to save in the dict)
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            group.save()

        # Loop models in group
        for model in groups_permissions[group_name]:
            # if model_class is written as dotted str, convert it to class
            if type(model) is str:
                model_class = apps.get_model(model)
            else:
                model_class = model

            # Loop permissions in group/model

            for perm_name in groups_permissions[group_name][model]:

                # Generate permission name as Django would generate it
                codename = f"{perm_name}_{model_class._meta.model_name}"

                try:
                    # Find permission object and add to group
                    content_type = ContentType.objects.get(
                        app_label=model_class._meta.app_label,
                        model=model_class._meta.model_name.lower(),
                    )
                    perm = Permission.objects.get(
                        content_type=content_type,
                        codename=codename,
                    )
                    group.permissions.add(perm)
                    logger.info(
                        f"  Adding permission '{codename}' to group '{group.name}'"
                    )
                except Permission.DoesNotExist:
                    logger.critical(f"  ERROR: Permission '{codename}' not found.")


def str_to_bool(bool_str: str) -> bool:
    """returns True if bool_str is "true", else False."""
    return bool_str.lower() == "true"


def snake_case_to_spaces(string):
    return string.replace("_", " ")


image_types = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "gif": "GIF",
    "tif": "TIFF",
    "tiff": "TIFF",
}


def resize_image(image, width, height):
    """Resizes an image to a given width/height"""
    # thanks to https://stackoverflow.com/a/71919278/818131

    img = Image.open(image)
    if img.width > width or img.height > height:
        output_size = (width, height)
        img.thumbnail(output_size)
        img_filename = Path(image.file.name).name
        # get file extension
        img_suffix = Path(image.file.name).name.split(".")[-1]
        # Use file extension to determine  file type from the image_type's dictionary
        img_format = image_types[img_suffix]
        # Save resized image into the buffer with the correct file type
        buffer = BytesIO()
        img.save(buffer, format=img_format)
        # Wrap buffer in a File object
        file_object = File(buffer)
        # Save new resized file
        image.save(img_filename, file_object)


# ------------------ Date/Time functions ------------------
def round_down_time(time: time, unit: int):
    """Round down to the nearest 15 minutes"""
    minute = (time.minute // unit) * unit
    rounded_time = time.replace(minute=minute, second=0, microsecond=0)
    return rounded_time


def round_up_time(time: time, unit: int):
    """Round up to the nearest 15 minutes"""
    minute = (time.minute // unit) * unit + unit
    hour = time.hour
    if minute >= 60:
        minute -= 60
        hour += 1
    if hour == 24:
        hour = 0

    rounded_time = time.replace(hour=hour, minute=minute, second=0, microsecond=0)
    return rounded_time


def monthdelta(date: datetime, delta: int) -> datetime:
    # modified after https://stackoverflow.com/questions/3424899/return-datetime-object-of-previous-month
    m, y = (date.month + delta) % 12, date.year + ((date.month) + delta - 1) // 12
    if not m:
        m = 12
    d = min(date.day, calendar.monthrange(y, m)[1])

    return date.replace(year=y, month=m, day=d)


def django_locale_to_country_code(locale: tuple) -> str:
    locale_name_split = locale[0].split("_")
    if len(locale_name_split) == 2:
        return locale_name_split[1].upper()
    else:
        return locale_name_split[0].upper()
