import unittest
from FrontendRolP1 import API, LocalStorage

class TestFrontendAPI(unittest.TestCase):
    def setUp(self):
        LocalStorage.set_item('access_token', '')  # Asegurarse de que no hay token

    def test_register_invalid(self):
        response, status = API.register('', '', '')
        self.assertIn(status, [400, 500])
        self.assertIn('error', response)

    def test_login_invalid(self):
        response, status = API.login('wronguser', 'wrongpass')
        self.assertIn(status, [401, 400, 500])
        self.assertIn('error', response)

    def test_create_character_no_token(self):
        response, status = API.create_character('Test', 'Elfo', 'Mago', '...')
        self.assertEqual(status, 401)
        self.assertIn('error', response)

    def test_get_characters_no_token(self):
        response, status = API.get_characters()
        self.assertEqual(status, 401)
        self.assertIn('error', response)

if __name__ == '__main__':
    unittest.main()
