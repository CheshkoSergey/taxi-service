from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver


class PublicDriverTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required_list(self):
        res = self.client.get(reverse("taxi:driver-list"))

        self.assertNotEqual(res.status_code, 200)

    def test_login_required_create(self):
        res = self.client.get(reverse("taxi:driver-create"))

        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="passwordAAA11111",
            license_number="AAA11111",
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        response = self.client.get(reverse("taxi:driver-list"))
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
