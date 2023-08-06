from django.views.generic import DetailView, CreateView

from medux.core.forms import CreatePrescriptionForm
from medux.core.models import Dosage, MedicationRequest


class PrescriptionDetailView(DetailView):
    model = Dosage


class CreatePrescriptionView(CreateView):
    model = MedicationRequest
    # form_class = CreatePrescriptionForm
    fields = "__all__"
