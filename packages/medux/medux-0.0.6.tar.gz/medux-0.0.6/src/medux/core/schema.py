import graphene
from .models import User, Patient
from graphene_django import DjangoObjectType

from gdaps.graphene.api import IGrapheneSchema


# User
class UserType(DjangoObjectType):
    """MedUX's built-in User type"""

    class Meta:
        model = User


class UserQuery:
    users = graphene.List(UserType)

    @staticmethod
    def resolve_users(self, info, **kwargs):
        return User.objects.all()


class UserSchema(IGrapheneSchema):
    query = UserQuery


# Patients
class PatientType(DjangoObjectType):
    """A basic representation of a patient"""

    class Meta:
        model = Patient


class PatientQuery:
    patients = graphene.List(PatientType)

    @staticmethod
    def resolve_patients(self, info, **kwargs):
        return Patient.objects.all()


class PatientSchema(IGrapheneSchema):
    query = PatientQuery
