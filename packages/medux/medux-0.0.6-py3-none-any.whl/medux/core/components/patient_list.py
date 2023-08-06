from django_unicorn.components import UnicornView

from medux.core.models import Patient


class PatientListView(UnicornView):
    patient_list = Patient.objects.none()

    def load_table(self, params: dict):
        self.patient_list = Patient.objects.filter(**params)
