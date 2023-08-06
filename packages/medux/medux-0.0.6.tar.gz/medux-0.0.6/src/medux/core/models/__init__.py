# from .fhir import *
from .patient import *
from .datapacks import *
from .geo import *
from .medication import *
from .organizations import *
from .devices import *
from .observations import *
from medux.common.models import CommonUser


class User(CommonUser):
    """The MedUX user class"""

    # TODO: address

    @property
    def is_employee(self):
        """returns true if this user is an employee"""
        return hasattr(self, "employee")
