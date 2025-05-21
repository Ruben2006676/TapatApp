import unittest
from BackendRolP1 import app
from flask.testing import FlaskClient

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client: FlaskClient = self.app.test_client()
        self.app.testing = True

    def test_register_user(self):
        response = self.client.post('/register', json={
            "username": "testuser",
            "password": "testpass",
            "email": "testuser@example.com"
        })
        self.assertIn(response.status_code, [201, 400])  # Puede ser 400 si ya existe
        self.assertIn('message', response.json or response.json.keys() if response.status_code == 201 else 'error')

    def test_login_user(self):
        response = self.client.post('/login', json={
            "username": "testuser",
            "password": "testpass"
        })
        self.assertIn(response.status_code, [200, 401])
        if response.status_code == 200:
            self.assertIn("access_token", response.json)

    def test_create_character_unauthenticated(self):
        response = self.client.post('/characters', json={
            "name": "TestChar",
            "race": "Elfo",
            "class": "Mago"
        })
        self.assertEqual(response.status_code, 401)  # No JWT


if __name__ == '__main__':
    unittest.main()
