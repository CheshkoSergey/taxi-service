from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer


class PublicCarTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required_list(self):
        res = self.client.get(reverse("taxi:car-list"))

        self.assertNotEqual(res.status_code, 200)

    def test_login_required_create(self):
        res = self.client.get(reverse("taxi:car-create"))

        self.assertNotEqual(res.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="passwordAAA11111",
            license_number="AAA11111",
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name_01",
            country="country_01"
        )

        Car.objects.create(
            model="test_model_01",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="test_model_02",
            manufacturer=manufacturer
        )

        response = self.client.get(reverse("taxi:car-list"))
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")
