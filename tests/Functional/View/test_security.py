from django.test import TestCase
from django.test import Client


class SecurityTest(TestCase):
    fixtures = ['fixture.json']
    
    def setUp(self):
        self.client = Client()

    def test_details(self):
        response = self.client.get("/registreren")

        self.assertEqual(response.status_code, 200)

        response = self.client.post('/registreren', {'username': 'Test','email': 'test@test.nl',
                                         'password': 'secret','password_repeat':'secret'})

        self.assertEqual(response.status_code, 302)

        response = self.client.get('/uitloggen')

        self.assertEqual(response.status_code, 302)

        response = self.client.post('/inloggen')

        self.assertEqual(response.status_code, 200)

        response = self.client.post('/inloggen', {'username': 'Test', 'password': 'secret'})

        self.assertEqual(response.status_code, 302)

        response = self.client.get('/verander-wachtwoord')

        self.assertEqual(response.status_code, 200)

        response = self.client.post('/verander-wachtwoord', {'password': 'secret', 'password_repeat': 'secret'})

        self.assertEqual(response.status_code, 302)