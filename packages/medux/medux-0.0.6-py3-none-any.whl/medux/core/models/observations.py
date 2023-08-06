from enum import Enum

from django.db import models
from django.utils.translation import gettext_lazy as _

from . import Coding
from ..fields import CodeField, PeriodField, QuantityField
from medux.common.models import BaseModel


class ObservationStatus(Coding):
    code_system_name = "observation-status"


# https://hl7.org/fhir/observation.html#Observation
class Observation(BaseModel):
    """Measurements and simple assertions made about a patient,
    device or other subject.

    .. note:

        IMPORTANT: inheriting classes must implement at least the "value" field for reading!
        This could be done as simple CharField, or as a property method that gets the value
        from more specific fields.

    Use cases:

    * Vital signs such as body weight, blood pressure, and temperature
    * Laboratory Data like blood glucose, or an estimated GFR
    * Imaging results like bone density or fetal measurements
    * Clinical Findings such as abdominal tenderness
    * Device measurements such as EKG data or Pulse Oximetry data
    * Clinical assessment tools such as APGAR or a Glasgow Coma Score
    * Personal characteristics: such as eye-color
    * Social history like tobacco use, family support, or cognitive status
    * Core characteristics like pregnancy status, or a death assertion
    """

    # The status of the result value
    # http://hl7.org/fhir/ValueSet/observation-status
    status = CodeField(ObservationStatus)

    # The time or time-period the observed value is asserted as being true. For biological subjects -
    # e.g. human patients - this is usually called the "physiologically relevant time".
    # This is usually either the time of the procedure or of specimen collection, but very often the source
    # of the date/time is not known, only the date/time itself
    # Type: dateTime|Period|Timing

    effective_datetime = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_("Clinically relevant time for observation"),
    )

    # TODO: add keyword arguments
    effective_period = PeriodField(
        # blank=True,
        # help_text=_("Clinically relevant time-period for observation"),
    )

    encounter = models.ForeignKey(
        "Encounter",
        null=True,
        # blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    # The date and time this version of the observation was made available to
    # providers, typically after the results have been reviewed and verified
    issued = models.DateTimeField(blank=True, null=True)

    # Who was responsible for asserting the observed value as "true"
    # FIXME: + Patient, Person...
    performer = models.ForeignKey(
        "HealthServiceProvider",
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    # The information determined as a result of making the observation,
    # if the information has a simple value
    # Type: Quantity|str|bool|int|Range|Ratio|time|dateTime|Period
    # IMPORTANT: has to be implemented by inheriting Model classes
    # value = ...

    # Provides a reason why the expected value in the element Observation.value[x] is missing
    # dataAbsentReason = CodeableConceptField(
    #     "DataAbsentReason", null=True, related_name="+"
    # )

    # interpretation = CodeableConceptField(
    #     "Observation Interpretation", null=True, related_name="+"
    # )

    comment = models.CharField(max_length=255, blank=True)

    # see http://hl7.org/fhir/ValueSet/body-site
    # bodySite = CodeableConceptField("SNOMED CT Body Structures??", null=True)

    # method = models.ForeignKey("ObservationMethods", null=True, related_name="+")

    # specimen = models.ForeignKey(
    #     "Specimen", null=True, on_delete=models.SET_NULL, related_name="+"
    # )

    device = models.ForeignKey(
        "Device",
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    # derivedFrom = ManyReferenceField(
    #     "DocumentReference|ImagingStudy|"
    #     "Media|QuestionnaireResponse|"
    #     "Observation|Sequence"
    # )

    # component = models.ManyToManyField(Component)

    # referenceRange = models.ManyToManyField(ReferenceRange)

    # whether this observation is a group observation (e.g. a battery, a panel of
    # tests, a set of vital sign measurements) that includes the target as a
    # member of the group.
    # When using this element, an observation will typically have either a
    # value or a set of related resources, although both may be present in
    # some cases. For a discussion on the ways Observations can assembled in
    # groups together.
    def has_member(self):
        return False

    def __str__(self):
        if hasattr(self, "value"):
            return f"{self.velue}"
        else:
            return super().__str__()


class PatientObservation(Observation):
    """Observation that is taken from a patient."""

    subject = models.ForeignKey(
        "Patient",
        on_delete=models.CASCADE,
        related_name="+",
    )

    class Meta:
        abstract = True


class DeviceObservation(Observation):
    """Observation that is taken from a device."""

    subject = models.ForeignKey(
        "Device",
        on_delete=models.CASCADE,
        related_name="+",
    )

    class Meta:
        abstract = True


# class BloodPressure(PatientObservation):
#     value=RatioField()


class BloodPressure(PatientObservation):
    systolic = models.PositiveSmallIntegerField()
    diastolic = models.PositiveSmallIntegerField()

    def value(self):
        return f"{self.systolic}/{self.diastolic}"


class BodyWeight(PatientObservation):
    value = QuantityField(max_digits=8, decimal_places=2)


class BodyTemperature(PatientObservation):
    value = QuantityField(max_digits=3, decimal_places=1)
