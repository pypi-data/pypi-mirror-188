"""
MedUX - A Free/OpenSource Electronic Medical Record
Copyright (C) 2017-2022 Christian González

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# TODO: Fields could be done better, see http://build.fhir.org/datatypes.html
# These types should be implemented very carefully, with all the validators
# and custom behaviours in place.
__author__ = "Christian González <christian.gonzalez@nerdocs.at>"

import base64
from datetime import timedelta
from decimal import Decimal
from enum import Enum
from uuid import uuid4

from composite_field import CompositeField
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from django.db.models import ForeignKey
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from enumfields import EnumField

from .validators import CodeValidator, OidValidator, IdValidator


class OptionalTimeDateTimeField(models.DateTimeField):
    """Field that optionally uses the time format.

    Set MEDUX["BIRTHDAY_FORMAT"] in settings.py to either "Date" or "DateTime" to use the desired format.
    """

    def formfield(self, **kwargs):
        field = None
        try:
            if settings.MEDUX["BIRTHDAY_FORMAT"] == "Date":
                field = "forms.DateField"
            elif settings.MEDUX["BIRTHDAY_FORMAT"] == "DateTime":
                field = "forms.DateTimeField"
            else:
                raise ImproperlyConfigured(
                    f"MEDUX['BIRTHDAY_FORMAT'] settings variable contains wrong value '{settings.MEDUX['BIRTHDAY_FORMAT']}'. Please set it to 'Date' or 'DateTime'."
                )
        except AttributeError:
            raise ImproperlyConfigured(
                "MEDUX settings variable does not contain a 'BIRTHDAY_FORMAT'. Please set it to 'Date' or 'DateTime'."
            )
        # FIXME: DateField is ignored in Admin
        return super().formfield(
            **{
                "form_class": field,
                **kwargs,
            }
        )


class Base64TextField(models.TextField):
    """A stream of bytes, base64 encoded"""

    # TODO: +RegexValidator '(\s*([0-9a-zA-Z\+\=]){4}\s*)+'
    def from_db_value(value):
        """Returns a str from the database value,
        which is encoded as base64 string"""

        if value is None:
            return None
        else:
            return base64.b64decode(value).decode("utf-8")

    # TODO: read only yet


class StringListField(models.TextField):
    """Represents a list of strings.

    in FHIR resources, there is often a string[0..*] needed. As Django
    Doesn't provide a string list field, this is a simple implementation.
    Other implementations would be possible using JSONfield on PostGreSQL."""

    # TODO: implement this field completely.
    # TODO: Beware of strings >255 chars
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # def to_python(self, value):
    #     """Normalize data to a list of strings."""
    #     # Return an empty list if no input was given.
    #     if not value:
    #         return []
    #     return value.split("\n")


class InstantField(models.DateTimeField):
    """An instant in time

    It must be known at least to the second and always includes a time zone.
    Note: This type is for system times, not human times."""

    def __init__(self, *args, **kwargs):
        kwargs["validators"] = [
            RegexValidator(
                r"([0-9]([0-9]([0-9][1-9]|[1-9]0)|"
                r"[1-9]00)|[1-9]000)-(0[1-9]|1[0-2])-"
                r"(0[1-9]|[1-2][0-9]|3[0-1])T([01][0-9]|2[0-3]):"
                r"[0-5][0-9]:"
                r"([0-5][0-9]|60)(\.[0-9]+)?(Z|(\+|-)"
                r"((0[0-9]|1[0-3]):[0-5][0-9]|14:00))"
            )
        ]
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        del kwargs["validators"]
        return name, path, args, kwargs


class UriField(models.URLField):
    """A Uniform Resource Identifier Reference.

    This is a URI, as defined in RFC 3986: https://tools.ietf.org/html/rfc3986
    Note: URIs generally are case sensitive. For an UUID like
    (urn:uuid:ad1b1c1b-96b0-4c4d-a826-2b6e31f0512b) use all lowercase letters!
    """

    # TODO: implementation
    def __init__(self, *args, **kwargs):
        # FIXME: we set this to an arbitrary 255 char string as max. could be more specific
        kwargs["max_length"] = 255
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs


class UrlField(UriField):
    """A Uniform Resource Locator (RFC 1738 ).

    Note: URLs are accessed directly using the specified protocol.
    Common URL protocols are http(s):, ftp:, mailto: and mllp:,
    though many others are defined.
    """


class CanonicalField(UriField):
    """A URI that refers to a canonical URI.

    The canonical type differs from a uri in that it has special meaning
    in this specification, and in that it may have a version appended,
    separated y a vertical bar (|).

    URIs can be absolute or relative, and may have an optional fragment
    identifier.
    This data type can be bound to a value set
    """


class CodeField(ForeignKey):
    """This is basically a Foreignkey with on_delete=PROTECT as default"""

    def __init__(self, to, **kwargs):
        # always protect deleting of related objects.
        # maybe later use an upgrade path in case of FHIR deletes a code?
        super().__init__(
            to, on_delete=kwargs.pop("on_delete", models.PROTECT), **kwargs
        )


class OidField(UriField):
    """An OID represented as a URI"""

    def __init__(self, *args, **kwargs):
        kwargs["validators"] = [OidValidator]
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["validators"]
        return name, path, args, kwargs


class IdField(models.CharField):
    """A field that can be used for an ID of an Object.

    Any combination of upper or lower case ASCII letters ('A'..'Z', and 'a'..'z',
    numerals ('0'..'9'), '-' and '.', with a length limit of 64 characters.
    This might be an integer, an un-prefixed OID, UUID or any other identifier
    pattern that meets these constraints."""

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 64
        kwargs["default"] = uuid4
        kwargs["validators"] = [IdValidator]
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        del kwargs["default"]
        del kwargs["validators"]
        return name, path, args, kwargs


class MarkdownField(models.TextField):
    """A string that *may* contain markdown syntax.

    This can be used for optional processing by a markdown presentation engine"""

    # TODO: implement Validator: \s*(\S|\s)*


class NarrativeStatus(Enum):
    GENERATED = "generated"
    EXTENSIONS = "extensions"
    ADDITIONAL = "additional"
    EMPTY = "empty"


class PeriodField(CompositeField):
    description = "A Field representing a period in time, with optional start or end."

    # Constraints: One of [start|end] must be given.

    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)

    # def __repr__(self):
    #     return Period(start=self.start, end=self.end)

    def timedelta(self) -> timedelta:
        return self.end - self.start


class UnitField(models.CharField):
    description = "A field which stores units."

    def __init__(self, **kwargs):
        kwargs.setdefault("max_length", 10)
        super().__init__(**kwargs)


class QuantityField(CompositeField):
    COMPARATORS = (
        ("<", _("<")),
        ("<=", _("<=")),
        (">=", _(">=")),
        (">", _(">")),
    )

    description = (
        "A field which stores value and (optionally) unit of a quantity., e.g. '250 ml'"
    )

    value = models.DecimalField(max_length=None, decimal_places=None)
    unit = UnitField(blank=True)
    system = models.CharField(max_length=255, blank=True)
    # code = CodeField(terminology_binding=...)  # The (FHIR) preferred system is UCUM
    comparator = models.CharField(max_length=2, blank=True, choices=COMPARATORS)

    def __init__(
        self,
        max_digits: int | None,
        decimal_places: int | None,
        verbose_name: str = None,
        blank: bool = False,
        default: Decimal = None,
        validators=None,
    ):
        super().__init__()
        self.verbose_name = verbose_name
        value = self["value"]
        value.blank = blank
        value.decimal_places = decimal_places
        value.max_digits = max_digits
        value.null = blank
        value.blank = blank
        self._validators = validators
        if default is not None:
            self.value.default = default.real

    def __str__(self):
        return f"{self.value} {self.unit}"

    # def clean(self, value, model_instance):
    #     """
    #     We need to run validation against ``Quantity`` instance.
    #     """
    #     output = self.to_python(value)
    #     self.validate(value, model_instance)
    #     self.run_validators(value)
    #     return output

    @cached_property
    def validators(self):
        # Default ``DecimalValidator`` doesn't work with ``Quantity`` instances.
        # FIXME use correct validators
        return super().validators + [self._validators]

    def formfield(self, **kwargs):
        defaults = {
            "form_class": "core.QuantityFormField",
            "decimal_places": self.value.decimal_places,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)


class RatioField(CompositeField):
    """A relationship between two Quantity values.

    Examples where a Ratio is used are:

    * titers (e.g. 1:150)
    * concentration ratios where the denominator is significant (e.g. 5mg/dl)
    * observed frequencies (e.g. 2 repetitions/8 hr)
    """

    numerator = QuantityField(
        max_digits=1, decimal_places=1, blank=True
    )  # 1=placeholder
    denominator = QuantityField(
        max_digits=1, decimal_places=1, validators=[MinValueValidator(0)]
    )  # 1=placeholder

    def __init__(
        self,
        num_max_digits: int,
        num_decimal_places: int,
        denom_max_digits: int,
        denom_decimal_places: int,
        verbose_name: str = None,
        blank: bool = False,
        validators=None,
    ):
        super().__init__()
        self.verbose_name = verbose_name

        numerator = self["numerator"]
        numerator.max_digits = num_max_digits
        numerator.decimal_places = num_decimal_places

        denominator = self["denominator"]
        denominator.max_digits = denom_max_digits
        denominator.decimal_places = denom_decimal_places

        numerator.blank = blank
        denominator.blank = blank
        denominator.null = False  # TODO: make sure null works here
        self._validators = validators

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"


# ======================== Unused Fields from FHIR ========================


# ===================== Primitive types =====================
# Primitive types are those with only a value,
# and no additional elements as children.
# see examples: http://build.fhir.org/datatypes-examples.html#primitives
# ===========================================================


# StringFields are implemented either as Textfields, or as Charfields,
# depending on how many chars (>255) are possible. Some databases do not
# implement more than 255 chars in a string.


# ===================== Complex types =====================
# In XML, these types are represented as XML Elements with child elements
# with the name of the defined elements of the type.
# The name of the element is defined where the type is used.
# In JSON, the data type is represented by an object with properties named
# the same as the XML elements. Since the JSON representation is almost
# exactly the same, only the first example has an additional explicit
# JSON representation.
#
# Complex data types may be "profiled".
# A Structure Definition or type "constraint" makes a set of rules about
# which elements SHALL have values and what the possible values are.
# ===========================================================


# class ManyReferenceField(models.ManyToManyField):
#     def __init__(self, to: str, **kwargs):
#
#         self.allowed_references = to.split("|")
#         for ref in self.allowed_references:
#             if ref not in fhir_server_allowed_references.split("|"):
#                 raise exceptions.FieldError(
#                     _("'{}' is not allowed as reference in {}".format(ref, "<FIXME>"))
#                 )
#
#         # No matter what this field should (dynamically) refer to,
#         # always make sure the Foreign key is bound to a "Reference" object
#         kwargs["to"] = "Reference"
#         super().__init__(**kwargs)
#
#     def deconstruct(self):
#         name, path, args, kwargs = super().deconstruct()
#         kwargs["to"] = "|".join(self.allowed_references)
#         return name, path, args, kwargs


# class CodeableConceptField(models.ForeignKey):
#     def __init__(self, value_set: str, *args, **kwargs):
#         assert type(value_set) == str
#
#         self.allowed_codings = value_set.split("|")
#
#         # always refer to the model "CodeableConcept", no matter what is given
#         kwargs["to"] = "CodeableConcept"
#
#         # FIXME: is SET_NULL ok everywhere?
#         kwargs["null"] = True
#         kwargs["on_delete"] = models.SET_NULL
#         super().__init__(*args, **kwargs)
#
#     def deconstruct(self):
#         name, path, args, kwargs = super().deconstruct()
#         del kwargs["null"]
#         kwargs["value_set"] = "|".join(self.allowed_codings)
#         return name, path, args, kwargs


# class PositiveIntField(models.PositiveIntegerField):
#     description = _("Positive integer >= 1")
#
#     def formfield(self, **kwargs):
#         defaults = {"min_value": 1}
#         defaults.update(kwargs)
#         return super().formfield(**defaults)


# class UnsignedIntField(models.PositiveIntegerField):
#     description = _("Positive integer >= 0")
#
#     # this is the Django implementation of PositiveIntegerField


# http://hl7.org/fhir/narrative-status
# FIXME: implement/import as ValueSet


# ======================== Special data types ========================


# class ReferenceField(models.ForeignKey):
#     """A field that holds a Foreignkey to a Reference Object,
#     which points to another FHIR Resource
#
#     At least one of reference, identifier and display SHALL be present
#     (unless an extension is provided).
#     The Reference object should return the real object.
#     FIXME this has to be coded in Django, does not work yet.
#     """
#
#     # This regex is true if the reference to a resource is consistent with a FHIR API
#     fhir_server_abs_url_conformance = (
#         r"((http|https)://([A-Za-z0-9\\\.\:\%\$]\/)*)?("
#         + fhir_server_allowed_references
#         + ")\/[A-Za-z0-9\-\.]{1,64}(\/_history\/[A-Za-z0-9\-\.]{1,64})?"
#     )
#
#     description = _("A dynamic reference to another Resource")
#
#     def __init__(self, to: str, **kwargs):
#         """Creates a new Reference Field.
#
#         The 'to' parameter is always overwritten and set to "Reference",
#         as the Reference db table works as intermediate mapper to the "real"
#         reference where this field points to.
#
#         Note: the 'on_delete' parameter must be set manually, as it could
#         change according to the context.
#         :param str to: one or more possible FHIR resources where an object
#             could point to. If there are more than one, use '|' as separator.
#             Example: 'Patient|Practitioner|Organization'
#         :raises FieldError: if the 'to' parameter is a not allowed resource.
#         """MarkdownField
#
#         assert type(to) == str
#
#         self.allowed_references = to.split("|")
#         for ref in self.allowed_references:
#             if ref not in fhir_server_allowed_references.split("|"):
#                 raise exceptions.FieldError(
#                     _("'{}' is not allowed as reference in {}".format(ref, "<FIXME>"))
#                 )
#
#         # No matter what this field should (dynamically) refer to,
#         # always make sure the Foreign key is bound to a "Reference" object
#         kwargs["to"] = "Reference"
#         super().__init__(**kwargs)
#
#     def deconstruct(self):
#         name, path, args, kwargs = super().deconstruct()
#         kwargs["to"] = "|".join(self.allowed_references)
#         return name, path, args, kwargs


# class NarrativeField(models.TextField):
#
#     # http://hl7.org/fhir/ValueSet/narrative-status
#     # general, extensions, additional, empty
#     status = models.CharField(max_length=35, choices=NARRATIVE_STATUS)
#
#     # TODO: implement a XHTMLField
#     # The XHTML content SHALL NOT contain a head, a body element, external stylesheet references,
#     # deprecated elements, scripts, forms, base/link/xlink, frames, iframes, objects or event related attributes
#     # (e.g. onClick).This is to ensure that the content of the narrative is contained within the resource
#     # and that there is no active content. Such content would introduce security issues and potentially safety
#     # issues with regard to extracting text from the XHTML.
#     div = models.TextField(null=False, blank=False)


# def validate_quantity_value(value):
#     """
#     Valid value for Quantity are:
#       - Single numeric value
#       - Quantity instances
#       - Pairs of numeric value and unit. unit can't be None.
#     """
#     if isinstance(value, (list, tuple)) and (len(value) != 2 or value[1] is None):
#         raise ValidationError(
#             f"Invalid value for QuantityField: {value}.",
#             code="invalid",
#         )
#
