from django.test import TestCase

from medux.core.models import (
    Physician,
    Patient,
    Person,
    MaritalStatusChoices,
    AdministrativeGender,
    Name,
)
from medux.core.models.patient import PatientRelationship

# tests created with ChatGPT (just for testing...)


class PatientModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.jane_name = Name.objects.create(first_name="Jane", last_name="Doe")
        cls.john_name = Name.objects.create(first_name="John", last_name="Doe")

        cls.jane = Person.objects.create()
        cls.jane.names.add(cls.jane_name)
        cls.john = Person.objects.create()
        cls.john.names.add(cls.john_name)

    def setUp(self):
        self.male_gender = AdministrativeGender.objects.create(code="male")
        self.person = Person.objects.create(
            birth_date="1990-01-01", gender=self.male_gender
        )
        self.person.names.add(self.jane_name)
        self.patient = Patient.objects.create(
            person=self.person,
            marital_status=MaritalStatusChoices.DIVORCED,
            emergency_contact_freetext="Contact in case of emergency: 555-555-5555",
        )

    def test_patient_creation(self):
        """Test patient object is created successfully"""
        self.assertTrue(isinstance(self.patient, Patient))
        self.assertEqual(self.patient.person.name, "John Doe")
        self.assertEqual(self.patient.marital_status, MaritalStatusChoices.DIVORCED)
        self.assertEqual(
            self.patient.emergency_contact_freetext,
            "Contact in case of emergency: 555-555-5555",
        )

    def test_str_method(self):
        """Test __str__ method of Patient model"""
        self.assertEqual(str(self.patient), "John Doe")

    def test_general_practitioner_field(self):
        """Test general_practitioner field of Patient model"""
        physician = Physician.objects.create(name="Dr. Smith")
        self.patient.general_practitioner = physician
        self.patient.save()
        self.assertEqual(self.patient.general_practitioner, physician)

    def test_physicians_field(self):
        """Test physicians field of Patient model"""
        physician1 = Physician.objects.create(name="Dr. Smith")
        physician2 = Physician.objects.create(name="Dr. Jones")
        self.patient.physicians.add(physician1, physician2)
        self.assertQuerysetEqual(
            self.patient.physicians.all(),
            ["<Physician: Dr. Smith>", "<Physician: Dr. Jones>"],
            ordered=False,
        )

    def test_related_persons_field(self):
        """Test related_persons field of Patient model"""
        patient1 = Patient.objects.create(person=self.jane)
        patient2 = Patient.objects.create(
            person=Person.objects.create(name="Bob Smith")
        )
        PatientRelationship.objects.create(
            from_patient=self.patient, to_patient=patient1
        )
        PatientRelationship.objects.create(
            from_patient=self.patient, to_patient=patient2
        )
        self.assertQuerysetEqual(
            self.patient.related_persons.all(),
            ["<Patient: Jane Doe>", "<Patient: Bob Smith>"],
            ordered=False,
        )

    def test_emergency_contact_field(self):
        """Test emergency_contact field of Patient model"""

        contact2 = Person.objects.create()
        contact2.names.add(Name.objects.create(first_name="Bob", last_name="Smith"))
        self.patient.emergency_contact.add(contact2)
        self.assertEqual(
            str(self.patient.emergency_contact.first().name),
            "SMITH, Bob",
        )
