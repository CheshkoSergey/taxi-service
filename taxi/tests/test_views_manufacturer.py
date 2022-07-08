from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer


class PublicManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required_list(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertNotEqual(res.status_code, 200)

    def test_login_required_create(self):
        res = self.client.get(reverse("taxi:manufacturer-create"))

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="passwordAAA11111",
            license_number="AAA11111",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="test_name_01",
            country="country_01"
        )
        Manufacturer.objects.create(
            name="test_name_02",
            country="country_02"
        )

        response = self.client.get(reverse("taxi:manufacturer-list"))
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
