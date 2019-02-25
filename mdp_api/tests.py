from django.http import HttpResponseNotAllowed
from django.test import Client, TestCase
from django.urls import reverse

from . import views


client = Client()


class ViewsTestCase(TestCase):

    def test_json_signup(self):
        response = client.get(reverse('json_signup'))
        self.assertIsInstance(response, HttpResponseNotAllowed)

        # Creating a user works.
        response = client.post(reverse('json_signup'), {
            'username': 'john',
            'email': 'john@doe.net',
            'password1': 'smith',
            'password2': 'smith',
        }, content_type="application/json")
        self.assertEqual(response.status_code, 201)

        # Creating a user with the same username does not.
        response = client.post(reverse('json_signup'), {
            'username': 'john',
            'email': 'otherjohn@doe.net',
            'password1': 'smith',
            'password2': 'smith',
        }, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'username')

        # Creating a user with the same email also does not.
        response = client.post(reverse('json_signup'), {
            'username': 'other_john',
            'email': 'john@doe.net',
            'password1': 'smith',
            'password2': 'smith',
        }, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'email')
