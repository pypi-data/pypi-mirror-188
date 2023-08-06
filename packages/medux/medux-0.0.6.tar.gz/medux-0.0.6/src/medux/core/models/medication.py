from enum import Enum

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..fields import CodeField, PeriodField, QuantityField, RatioField
from .organizations import HealthServiceProvider
from .fhir import Coding, EpisodeOfCare
from medux.common.models import BaseModel
from .datapacks import PackageDataModel


class MedicationStatus(Coding):
    code_system_name = "medication-status"
    # comment = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = _("Medication Statuses")


class MedicationRoute(PackageDataModel):
    pass


class MedicationMethod(Coding):
    pass


# http://terminology.hl7.org/CodeSystem/dose-rate-type
class DoseRateType(Coding):
    code_system_name = "dose-rate-type"


# https://www.hl7.org/fhir/dosage.html
class Dosage(models.Model):

    # sequence
    text = models.CharField(
        max_length=255, help_text=_("Free text dosage instructions e.g. '1x/day'")
    )
    additional_instructions = models.CharField(
        max_length=255,
        help_text=_(
            "Supplemental instruction or warnings to the patient - e.g. 'with meals', 'may cause drowsiness'"
        ),
        blank=True,
    )
    patient_instructions = models.CharField(
        max_length=255,
        help_text=_("Instructions in terms that are understood by the patient"),
        blank=True,
    )

    as_needed = models.BooleanField(
        default=False, help_text="Take 'as needed' (for ...)"
    )
    # as_needed_concept : e.g. "Headache"
    # could be a CharField too.

    route = models.ForeignKey(MedicationRoute, on_delete=models.PROTECT)
    # maxDosePerPeriod

    method = models.ForeignKey(
        MedicationMethod,
        blank=True,
        null=True,
        help_text=_("Technique for administering medication"),
        on_delete=models.SET_NULL,
    )

    dose_type = CodeField(DoseRateType, default="ordered")
    # dose_range = models.RangeField()
    dose_quantity = QuantityField(max_digits=10, decimal_places=2, blank=True)

    # rate ratio
    dose_rate = RatioField(
        num_max_digits=10,
        num_decimal_places=2,
        denom_max_digits=10,
        denom_decimal_places=2,
        blank=True,
    )

    def __str__(self):
        return self.text


class Ingredient(models.Model):  # PackageDataModel
    pass


class MedicationTerminologySystem(PackageDataModel):
    """A Medication terminology system like SNOMED, Austrian PZN (Pharmazentralnummer), etc."""

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class MedicationForm(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# https://www.hl7.org/fhir/medication.html
class Medication(PackageDataModel):
    """Definition of a medication for the purposes of prescribing, dispensing, and administering."""

    code_system = models.ForeignKey(
        MedicationTerminologySystem,
        help_text=_("The defining coding system"),
        on_delete=models.PROTECT,
    )
    code = models.CharField(
        max_length=64,
        help_text=_("The medication code within this coding system"),
    )

    status = CodeField(
        MedicationStatus,
        default="active",
    )

    manufacturer = models.ForeignKey(
        HealthServiceProvider,
        on_delete=models.PROTECT,
        help_text=_("Manufacturer of the medication product. (Not the distributor.)"),
    )

    # e.g. powder | tablets | capsule
    form = models.ForeignKey(MedicationForm, on_delete=models.PROTECT)

    # Amount
    # TODO: amount nominator/denominator for ratios?
    # see https://www.hl7.org/fhir/medication.html, https://www.hl7.org/fhir/datatypes.html#Ratio and
    # https://www.hl7.org/fhir/datatypes.html#Quantity
    amount_value = models.DecimalField(
        decimal_places=3, max_digits=10, help_text=_("Amount of drug in package")
    )
    amount_unit = models.CharField(max_length=25, help_text=_("Unit representation"))
    # TODO: use FK instead of code?
    amount_unit_code = models.CharField(max_length=255)

    ingredients = models.ManyToManyField(Ingredient)

    # Batch / Package information (optional)
    batch_lot_number = models.CharField(
        max_length=255, blank=True, help_text=_("Identifier assigned to batch")
    )
    batch_expiration_date = models.DateField(
        blank=True, help_text=_("When batch will expire")
    )


# MedicationStatement is not needed ATM
#
# https://www.hl7.org/fhir/medicationstatement.html
# class MedicationStatement(BaseModel):
#     """Basically a line in a list of prescribed medications.
#
#     The MedicationStatement resource is used to record medications or substances that ``the patient reports``
#     as being taken, not taking, have taken in the past or may take in the future.
#     It can also be used to record medication use that is derived from other records such as a MedicationRequest.
#
#     The statement is not used to request or order a medication. When requesting medication, when there is
#     a patient focus or instructions regarding their use, a MedicationRequest, SupplyRequest or DeviceRequest
#     should be used instead
#     """
#
# class Status(Enum):
#     active = _("active")
#     completed = _("completed")
#     entered_in_error = _("entered in error")
#     intended = _("intended")
#     stopped = _("stopped")
#     on_hold = _("on-hold")
#     unknown = _("unknown")
#     not_taken = _("not-taken")
#
#     status = CodeField(terminology_binding=Status)
#     patient = models.ForeignKey("Patient", on_delete=models.CASCADE)
#     medication = models.ForeignKey(Medication, on_delete=models.PROTECT)
#     encounter = models.ForeignKey(
#         "Encounter",
#         help_text=_("Encounter associated with MedicationStatement"),
#         on_delete=models.PROTECT,
#     )
#     episode = models.ForeignKey(
#         EpisodeOfCare,
#         help_text=_("EpisodeOfCare associated with MedicationStatement"),
#         on_delete=models.PROTECT,
#     )
#     note = models.TextField()


# http://hl7.org/fhir/codesystem-medicationrequest-course-of-therapy.html
class CourseOfTherapy(Coding):
    # Medication request course of therapy codes:
    name = "medicationrequest-course-of-therapy"


# https://hl7.org/fhir/valueset-medicationrequest-status.html
class RequestStatus(Coding):
    code_system_name = "medicationrequest-status"


class RequestPriority(Coding):
    code_system_name = "request-priority"


class MedicationRequestIntent(Coding):
    code_system_name = "medicationrequest-intent"


# https://www.hl7.org/fhir/medicationrequest.html
class MedicationRequest(BaseModel):
    """Orders for medications for a patient.

    Basically a "prescription" of one medication for outpatients."""

    status = CodeField(RequestStatus)
    # status_reason = models.ForeignKey(MedicationRequestStatusReason, on_delete=models.PROTECT)

    # Whether the request is a proposal, plan, or an original order
    intent = CodeField(MedicationRequestIntent)

    # inpatient, outpatient, community, discharge
    # see https://www.hl7.org/fhir/codesystem-medicationrequest-category.html
    # category = models.ForeignKey(MedicationRequestCategory, on_delete=models.PROTECT)

    priority = CodeField(RequestPriority)
    do_not_perform = models.BooleanField(
        default=False, help_text=_("True if request is prohibiting action")
    )

    reported = models.BooleanField(default=False)

    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)

    subject = models.ForeignKey(
        "Patient",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=_("Who medication request is for"),
    )

    encounter = models.ForeignKey("Encounter", on_delete=models.CASCADE)

    # = created
    # authored_on = models.DateTimeField(auto_now=True)

    # TODO: requester: Person/Organization/Device
    requester = models.ForeignKey(
        HealthServiceProvider,
        on_delete=models.SET_NULL,
        null=True,
        help_text=_("Who requested the request"),
    )

    # default: current user
    recorder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # reason_code, reason_reference ...

    based_on = models.ForeignKey("CarePlan", null=True, on_delete=models.SET_NULL)

    # priorPrescription
    replaces = models.ForeignKey(
        "MedicationRequest",
        on_delete=models.PROTECT,
        help_text=_("An order/prescription that is being replaced"),
        related_name="replaced_by",
    )

    course_of_therapy_type = models.ForeignKey(
        CourseOfTherapy, on_delete=models.PROTECT, blank=True
    )

    note = models.CharField(
        max_length=255, help_text=_("Information about the prescription")
    )

    dosage_instruction = models.OneToOneField(Dosage, on_delete=models.PROTECT)


class CarePlanIntent(Coding):
    code_system_name = "care-plan-intent"


class CarePlan(BaseModel):
    """based upon the FHIR "CarePlan": https://hl7.org/fhir/careplan.html"""

    # based_on = models.ForeignKey(
    #     "CarePlan",
    #     null=True,
    #     on_delete=models.SET_NULL,
    #     help_text=_("Fulfills CarePlan"),
    #     related_name="parent",
    # )

    # part_of = models.ForeignKey(
    #     "CarePlan",
    #     null=True,
    #     on_delete=models.SET_NULL,
    #     help_text=_("Part of referenced CarePlan"),
    # )

    status = CodeField(RequestStatus)
    intent = CodeField(CarePlanIntent)

    replaces = models.ForeignKey(
        "CarePlan",
        null=True,
        on_delete=models.SET_NULL,
        help_text=_("CarePlan replaced by this CarePlan"),
        related_name="replaced_by",
    )

    # TODO: could be also Patient, RelatedPerson etc...
    author = models.ForeignKey(
        HealthServiceProvider, null=True, on_delete=models.SET_NULL
    )
    title = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Human-friendly name for the care plan"),
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Summary of plan"),
    )
    subject = models.ForeignKey("Patient", on_delete=models.CASCADE)

    # TODO: keep null=True? CarePlan is possible "dangling" without encounter?
    encounter = models.ForeignKey("Encounter", null=True, on_delete=models.SET_NULL)

    period = PeriodField()

    # careTeam, addresses, supportingInfo, goal, activity,

    note = models.TextField(blank=True, help_text=_("Comments about the plan"))


class MedicationPlan(CarePlan):
    """A medication plan that can be printed etc.

    Contains a list of medication requests, and could be printed, handed out to the patient, or given to another
    health care service worker.
    """

    medications = models.ManyToManyField(MedicationRequest)


# class DeviceRequest(Request):
#     pass


# https://www.hl7.org/fhir/medicationadministration.html
# class MedicationAdministration(BaseModel):
#     """Describes the event of a patient consuming or otherwise being administered a medication.
#     This may be as simple as swallowing a tablet or it may be a long running infusion.
#
#     Related resources tie this event to the authorizing prescription, and the specific encounter
#     between patient and health care practitioner."""
