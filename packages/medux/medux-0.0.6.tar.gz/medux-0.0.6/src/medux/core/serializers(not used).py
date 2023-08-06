"""
MedUX - A Free/OpenSource Electronic Medical Record
Copyright (C) 2017 Christian González

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

from rest_framework import serializers
from medux.core.models import Patient, Identity, Name, Address


class IdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Identity
        fields = [
            "pupic",
            "gender",
            "dob",
            "dob_is_estimated",
            "marital_status",
            "cob",
            "deceased",
            "title",
            "emergency_contact_freetext",
            "emergency_contact",
            "comment",
        ]


class NameSerializer(serializers.ModelSerializer):
    """
    {
        "use" : "<code>", // usual | official | temp | nickname | anonymous | old | maiden
        "text" : "<string>", // Text representation of the full name
        "family" : "<string>", // Family name (often called 'Surname')
        "given" : ["<string>"], // Given names (not always 'first'). Includes middle names
        "prefix" : ["<string>"], // Parts that come before the name
        "suffix" : ["<string>"], // Parts that come after the name
        "period" : { Period } // Time period when name was/is in use
    }
    """

    use = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()
    family = serializers.SerializerMethodField()
    given = serializers.SerializerMethodField()
    prefix = serializers.SerializerMethodField()
    suffix = serializers.SerializerMethodField()
    period = serializers.SerializerMethodField()

    def get_use(self, name):
        return "usual"  # Todo: This information is not beeing stored in the DB

    def get_text(self, name):
        return "{} {}".format(name.firstname, name.lastname)

    def get_family(self, name):
        return name.lastname

    def get_given(self, name):
        return name.firstname

    def get_prefix(self, name):
        return ""  # Todo: This information is not beeing stored in the DB

    def get_suffix(self, name):
        return ""  # Todo: This information is not beeing stored in the DB

    def get_period(self, name):
        return ""  # Todo: This information is not beeing stored in the DB

    class Meta:
        model = Name
        fields = [
            "use",
            "text",
            "family",
            "given",
            "prefix",
            "suffix",
            "period",
        ]


class ContactPointSerializer(serializers.ModelSerializer):
    """
    See http://build.fhir.org/datatypes.html#ContactPoint
    {
      "system" : "<code>", // C? phone | fax | email | pager | url | sms | other
      "value" : "<string>", // The actual contact point details
      "use" : "<code>", // home | work | temp | old | mobile - purpose of this contact point
      "rank" : "<positiveInt>", // Specify preferred order of use (1 = highest)
      "period" : { Period } // Time period when the contact point was/is in use
    }
    """

    system = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    use = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()
    period = serializers.SerializerMethodField()

    def get_system(self, identity):
        # Either phone | fax | email | pager | url | sms | other
        return "other"  # Todo: currently only the address is stored in the DB

    def get_value(self, identity):
        # The actual contact point details
        # Todo: since most of these fields are not required the address might be not valid
        """
        return ['{}, {}, {}, {}'.format(
            '{} ({}) {}'.format(address.street, address.aux_street,
                                address.number) if address.aux_street else '{} {}'.format(address.street,
                                                                                          address.number),
            address.postcode,
            address.city,
            address.state
        ) for address in identity.addresses]
        """
        return "not implemented"  # Todo

    def get_use(self, identity):
        return "home"

    def get_rank(self, identity):
        return (
            1  # There can only be one contact person. Therefore, this will always be 1
        )

    def get_period(self, identity):
        return ""  # Todo: This information is not beeing stored in the DB

    class Meta:
        model = Identity
        fields = [
            "system",
            "value",
            "use",
            "rank",
            "period",
        ]


class AddressSerializer(serializers.ModelSerializer):
    """
    {
      "use" : "<code>", // home | work | temp | old | billing - purpose of this address
      "type" : "<code>", // postal | physical | both
      "text" : "<string>", // Text representation of the address
      "line" : ["<string>"], // Street name, number, direction & P.O. Box etc.
      "city" : "<string>", // Name of city, town etc.
      "district" : "<string>", // District name (aka county)
      "state" : "<string>", // Sub-unit of country (abbreviations ok)
      "postalCode" : "<string>", // Postal code for area
      "country" : "<string>", // Country (e.g. can be ISO 3166 2 or 3 letter code)
      "period" : { Period } // Time period when address was/is in use
    }
    """

    use = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()
    line = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    postalCode = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    period = serializers.SerializerMethodField()

    def get_use(self, address):
        return "home"  # Todo: Should all addresses have the use 'home'?

    def get_type(self, address):
        return "both"  # Todo: Should all addresses have the type 'both'?

    def get_text(self, address):
        return address  # Todo: implement __str__()-method from address

    def get_line(self, address):
        # Street name, number, direction & P.O. Box etc.
        # Todo: What is meant with directions?
        # Todo: add P.O.-box
        return [address.street, address.number]

    def get_city(self, address):
        return address.city

    def get_disctrict(self, address):
        # District name (aka county)
        return ""  # Todo: What would that be in our case?

    def get_state(self, address):
        return address.state.name

    def get_postalCode(self, address):
        return str(address.postcode)

    def get_country(self, address):
        # Country (e.g. can be ISO 3166 2 or 3 letter code)
        return address.state.code

    def get_period(self, address):
        return ""  # Todo: This information is not beeing stored in the DB

    class Meta:
        model = Address
        fields = [
            "use",
            "type",
            "text",
            "line",
            "city",
            "district",
            "state",
            "postalCode",
            "country",
            "period",
        ]


class PatientSerializer(serializers.ModelSerializer):
    resourceType = serializers.SerializerMethodField()
    identifier = serializers.SerializerMethodField()
    active = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    telecom = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    birthdate = serializers.SerializerMethodField()
    deceasedBoolean = serializers.SerializerMethodField()
    deceasedDateTime = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    maritalStatus = serializers.SerializerMethodField()
    multipleBirthBoolean = serializers.SerializerMethodField()
    multipleBirthInteger = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    contact = serializers.SerializerMethodField()
    communication = serializers.SerializerMethodField()
    generalPractitioner = serializers.SerializerMethodField()
    managingOrganization = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()

    def get_resourceType(self, patient):
        return "Patient"

    def get_identifier(self, patient):
        """
        The identifier should have the following structure. See http://build.fhir.org/datatypes.html#Identifier for
        details.
        {
            "use" : "<code>", // usual | official | temp | secondary | old (If known)
            "type" : { CodeableConcept }, // Description of identifier
            "system" : "<uri>", // The namespace for the identifier value
            "value" : "<string>", // The value that is unique
            "period" : { Period }, // Time period when id is/was valid for use
            "assigner" : { Reference(Organization) } // Organization that issued id (may be just text)
        }
        """
        return "not implemented"  # Todo

    def get_active(self, patient):
        # Todo: Should return a boolean stating whether this patient's record is in active use or not
        return "not implemented"

    def get_name(self, patient):
        # The patient and the name object share the same identity.
        return NameSerializer(patient.identity.name_set.all(), many=True).data

    def get_telecom(self, patient):
        """
        A contact detail for the individual. See http://build.fhir.org/datatypes.html#ContactPoint for details.
        """
        return [ContactPointSerializer(patient.identity).data]

    def get_gender(self, patient):
        # Todo: label is a CharField and can therefore be anything.
        # Todo: But gender must be one of the following: male | female | other | unknown
        return patient.identity.gender.label

    def get_birthdate(self, patient):
        return patient.identity.dob.date()

    def get_deceasedBoolean(self, patient):
        return True if patient.identity.deceased else False

    def get_deceasedDateTime(self, patient):
        return patient.identity.deceased

    def get_address(self, patient):
        return AddressSerializer(patient.identity.addresses, many=True).data

    def get_maritalStatus(self, patient):
        return (
            patient.identity.marital_status.name
            if patient.identity.marital_status
            else ""
        )

    def get_multipleBirthBoolean(self, patient):
        return "not implemented"  # Todo

    def get_multipleBirthInteger(self, patient):
        return "not implemented"  # Todo

    def get_photo(self, patient):
        return "not implemented"  # Todo

    def get_contact(self, patient):
        return "not implemented"  # Todo

    def get_communication(self, patient):
        # Todo
        return [
            {
                "language": "not implemented",
                "preferred": "not implemented",
            }
        ]

    def get_generalPractitioner(self, patient):
        return "not implemented"  # Todo

    def get_managingOrganization(self, patient):
        return "not implemented"  # Todo

    def get_link(self, patient):
        return [
            {
                "other": "not implemented",  # Todo: The other patient or related person resource that the link refers to
                "type": "not implemented",  # Todo: replaced-by | replaces | refer | seealso - type of link
            }
        ]

    class Meta:
        model = Patient
        fields = [
            "resourceType",
            "identifier",
            "active",
            "name",
            "telecom",
            "gender",
            "birthdate",
            "deceasedBoolean",
            "deceasedDateTime",
            "address",
            "maritalStatus",
            "multipleBirthBoolean",
            "multipleBirthInteger",
            "photo",
            "contact",
            "communication",
            "generalPractitioner",
            "managingOrganization",
            "link",
        ]
