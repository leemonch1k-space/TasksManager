from django.test import TestCase

from landing.forms import RegistrationForm
from task.models import Position


class FormsTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="FormTester"
        )

    def test_registration_form_valid_data(self):
        form_data = {
            "username": "Bobinskiy",
            "first_name": "Bob",
            "last_name": "Bobchenko",
            "email": "Bobinskiy@gmail.com",
            "password1": "VeryStrongPassword1",
            "password2": "VeryStrongPassword1",
            "position": self.position,

        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registration_form_in_valid_data(self):
        form_data = {
            "username": "Bobinskiy",
            "first_name": "Bob",
            "last_name": "Bobchenko",
            "email": None,
            "password1": "VeryStrongPassword1",
            "password2": "VeryStrongPassword1",
            "position": None,

        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
