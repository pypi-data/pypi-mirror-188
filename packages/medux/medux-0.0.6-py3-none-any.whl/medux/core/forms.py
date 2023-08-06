from django import forms
from django.utils.translation import gettext_lazy as _

from medux.core.models import Dosage, MedicationRequest


class QuantityField(forms.CharField):
    widget = forms.widgets.TextInput


class DosageWidget(forms.TextInput):
    pass


class DosageForm(forms.ModelForm):
    class Meta:
        model = Dosage
        widgets = {"dose_rate_numerator_value": DosageWidget}
        fields = [
            "text",
            "additional_instructions",
            "patient_instructions",
            "as_needed",
            "route",
            "method",
            "dose_type",
            "dose_quantity_value",
            "dose_quantity_unit",
            # "dose_rate_nominator_value",
        ]


class CreatePrescriptionForm:
    model = MedicationRequest
