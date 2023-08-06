from django.core.exceptions import ValidationError
from django.test import TestCase

from medux.preferences.definitions import Scope
from medux.preferences.models import ScopedPreference


class ScopedPreferenceModelTestCase(TestCase):
    def test_create_model(self):
        m = ScopedPreference(
            namespace="foo", key="bar", scope=Scope.VENDOR, value="baz"
        )
        m.save()

        self.assertEqual(m.namespace, "foo")
        self.assertEqual(m.key, "bar")
        self.assertEqual(m.scope, Scope.VENDOR)

    def test_clean_lowercase(self):
        m = ScopedPreference(
            namespace="Foo", key="bAr", scope=Scope.VENDOR, value="baz"
        )
        m.clean()

        self.assertEqual(m.namespace, "foo")
        self.assertEqual(m.key, "bar")

    def test_clean_no_user(self):
        with self.assertRaises(ValidationError):
            m = ScopedPreference(
                namespace="foo", key="bar", scope=Scope.USER, value="baz"
            )
            m.clean()

    def test_clean_no_group(self):
        with self.assertRaises(ValidationError):
            m = ScopedPreference(
                namespace="foo", key="bar", scope=Scope.GROUP, value="baz"
            )
            m.clean()

    # def test_clean_no_device(self):
    #     with self.assertRises(ValidationError):
    #         m = ScopedPreference(
    #             namespace="foo", key="bar", scope=Scope.DEVICE, value="baz"
    #         )
    #         m.clean()

    def test_clean_no_tenant(self):
        with self.assertRaises(ValidationError):
            m = ScopedPreference(
                namespace="foo", key="bar", scope=Scope.TENANT, value="baz"
            )
            m.clean()
