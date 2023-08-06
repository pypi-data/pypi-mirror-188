from django.db.models import PositiveIntegerField
from django.utils.translation import gettext_lazy as _
from django.db import models

import medux.core.fields
from medux.common.models import CreatedModifiedModel, BaseModel
from .fhir import Coding, PackageDataModel, ContactPoint, AdministrativeGender
from .geo import Country, Address


class Specialty(PackageDataModel):
    """Medical field a physician operates in"""

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# https://terminology.hl7.org/CodeSystem/organization-type
class OrganizationType(Coding):
    pass


class Organization(PackageDataModel):
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    alias = medux.core.fields.StringListField(blank=True)

    # FIXME: should not be mandatory!
    # phone, fax, email etc.
    telecom = models.ManyToManyField(ContactPoint, blank=True)
    address = models.ForeignKey(
        Address, null=True, blank=True, on_delete=models.PROTECT, related_name="+"
    )

    def __str__(self):
        return self.name

    @property
    def type(self):
        """Implement this type for each inheriting class.

        See https://terminology.hl7.org/CodeSystem/organization-type for a list."""
        raise NotImplementedError

    def __get_item(self, system: str):
        """returns latest ContactPoint information of given system

        E.g. you can use Person.phone
        """
        # silently return nothing when given system is nonexistent.
        if system not in [key for key, value in ContactPoint.CONTACT_POINT_SYSTEM]:
            return ""

        items = self.telecom.filter(system=system)
        if items:
            # return first value that matches the given system
            return items.order_by("weight").first().value
        else:
            return ""

    @property
    def phone(self):
        return self.__get_item("phone")

    @property
    def email(self):
        return self.__get_item("email")


class Company(Organization):
    class Meta:
        verbose_name_plural = _("Companies")

    type = "other"


class InsuranceCompany(Company):
    """Either a private, or a social insurance company"""

    type = "ins"


class HealthServiceProvider(Organization):
    """A base class for Practitioner, Hospital/Department and other Health service providers."""

    type = "prov"


class Physician(HealthServiceProvider):
    """A Physician that is known to the user and can be referenced."""

    # name should be auto-generated from person

    type = "other"

    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    speciality = models.ForeignKey(
        Specialty,
        on_delete=models.PROTECT,
        help_text=_("Medical field"),
        related_name="physicians",
    )
    personal_salutation = models.CharField(
        max_length=100,
        help_text=_(
            "if you know this physician personally, you can choose to customize his salutation, "
            "like 'Dear Thomas,'"
        ),
        blank=True,
    )

    def __str__(self):
        return f"{self.person}"


class Hospital(HealthServiceProvider):
    """A Hospital representation which has many departments.

    see :class:`Department`
    """

    def type(self):
        # not specified in FHIR
        return "prov"


class Department(PackageDataModel):
    """A department in a hospital"""

    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name="departments"
    )
    name = models.CharField(max_length=255)
    # shortcut = models.CharField(max_length=10)

    # Here you can only provide the direct extension of the department.
    # the phone number will be calculated automatically using the hospital's
    # using phone()
    telecom = models.ManyToManyField(ContactPoint)

    def phone(self):
        hospital_phone = self.hospital.telecom.objects.get(
            system="phone"
        )  # type: ContactPoint
        extension = self.telecom.objects.get(system="phone")
        if hospital_phone.value and extension.value:
            return f"{hospital_phone.value} - {extension.value}"

    def __str__(self):
        return f"{self.hospital.name} - {self.name}"

    def type(self):  # noQa
        return "dept"


class Name(CreatedModifiedModel):
    """All the names a person is known under"""

    # As opposed to the versioning of all other tables,
    # changed names should not be soft-deleted.
    # Search functionality must be available at any time for all names a
    # person ever had.

    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    preferred = models.CharField(
        max_length=255,
        help_text=_(
            "preferred first name, the name a person is usually called (nickname)"
        ),
        blank=True,
        null=True,
    )
    comment = models.CharField(
        max_length=255,
        help_text=_(
            "a comment regarding this name, useful in things like 'name before marriage' etc."
        ),
        blank=True,
        null=True,
    )
    weight = PositiveIntegerField(default=1)

    def __str__(self):
        # TODO: make order configurable
        return f"{self.last_name.upper()}, {self.first_name}"

    class Meta:
        ordering = ["weight"]


class Person(BaseModel):
    """A generic, natural person, or identity

    A person is mostly in relation with a patient, like his caregiver, etc."""

    # patient = models.ForeignKey(
    #     "Patient",
    #     blank=True,
    #     on_delete=models.PROTECT,
    #     help_text=_("The patient this person is related to."),
    # )
    # relationship = models.ForeignKey(
    #     RelationType,
    #     on_delete=models.PROTECT,
    #     help_text=_(
    #         "The relation this person has to the patient, e.g. Caregiver, Taxi drier etc."
    #     ),
    # )
    names = models.ManyToManyField(Name)
    title = models.CharField(
        max_length=50, blank=True, null=True, help_text=_("Academic title")
    )
    gender = models.ForeignKey(
        AdministrativeGender, blank=True, null=True, on_delete=models.PROTECT
    )
    birth_date = models.DateField(
        verbose_name=_("Date of birth"), null=True, blank=True
    )
    birth_time = models.TimeField(
        verbose_name=_("Time of birth"), blank=True, null=True
    )
    birth_date_is_estimated = models.BooleanField(default=False)

    # country of birth as per date of birth, coded as 2 character ISO code
    # TODO: make choices=ISO3166 fixture
    country_of_birth = models.ForeignKey(
        Country,
        help_text=_("ISO code of Country of Birth"),
        on_delete=models.SET_NULL,
        null=True,
    )

    # date when a person has died
    deceased_date = models.DateField(
        verbose_name=_("Date of death"), blank=True, null=True
    )
    deceased_time = models.TimeField(
        verbose_name=_("Time of death"), blank=True, null=True
    )
    deceased_is_estimated = models.BooleanField(default=False)

    addresses = models.ManyToManyField(Address, through="AddressMapper")

    # FHIR: telecom
    telecom = models.ManyToManyField(
        ContactPoint,
        help_text=_(
            "A contact detail for the person, e.g. a telephone number or an email address"
        ),
    )
    photo = models.ImageField(blank=True)
    active = models.BooleanField(
        help_text=_("Whether this person's record is in active use."), default=True
    )

    # # TODO: implement generatePubic and set required=True
    # pupic = models.CharField(
    #     max_length=24,
    #     blank=True,
    #     null=True,
    #     help_text=_(
    #         "Portable Unique Person Identification Code as per GNUmed white papers"
    #     ),
    # )
    #
    # def generate_pupic(self):
    #     """Generates a Portable Unique Person Identification according to
    #     GNUmed definition"""
    #     # TODO: implement PUPIC generation
    #     raise NotImplementedError

    @property
    def name(self):
        """Returns latest concatenated full name of Person's names list"""
        # return first in the list of names
        # TODO: add title here?
        return self.names.order_by("weight").first()

    @property
    def first_name(self):
        """Returns latest firstname in Person's names list"""
        return self.name.first_name

    @property
    def last_name(self):
        """Returns latest lastname in Person's names list"""
        return self.name.last_name

    def __get_item(self, system: str):
        """returns latest ContactPoint information of given system

        E.g. you can use Person.phone
        """
        # silently return nothing when given system is nonexistent.
        if system not in [key for key, value in ContactPoint.CONTACT_POINT_SYSTEM]:
            return ""

        items = self.telecom.filter(system=system)
        if items:
            # return first value that matches the given system
            return items.order_by("weight").first().value
        else:
            return ""

    @property
    def phone(self):
        return self.__get_item("phone")

    @property
    def email(self):
        return self.__get_item("email")

    def __str__(self):
        return f"{self.name}, {self.birth_date}"


class ContactPerson(Person):
    """A contact person within a company."""

    organization = models.ForeignKey(
        Organization,
        null=True,
        on_delete=models.SET_NULL,
        related_name="contact_persons",
    )

    def __str__(self):
        return f"{self.organization}: {self.name}"
