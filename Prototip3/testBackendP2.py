import unittest
from flask import Flask, jsonify
from flask.testing import FlaskClient
from your_flask_app import app, Usuari, Nen, Tap, ServeiWeb, DAOUsuaris, DAONens, DAOTaps

class TestBackend(unittest.TestCase):

    # Configuración de la aplicación para pruebas
    def setUp(self):
        # Creamos un cliente de pruebas de Flask
        self.app: Flask = app
        self.client: FlaskClient = self.app.test_client()
        self.app.testing = True  # Activar el modo de testing

    # Test para la creación de un usuario
    def test_crear_usuari(self):
        response = self.client.post('/usuari', json={
            "nom_usuari": "nou_usuari",
            "contrasenya": "nova_contrasenya",
            "correu": "nou_usuari@gmail.com",
            "nom": "Nou",
            "cognom": "Usuari"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("Usuari creat amb èxit", response.json.get("missatge"))

    # Test para iniciar sesión
    def test_iniciar_sessio(self):
        response = self.client.post('/iniciar_sessio', json={
            "correu": "prova@gmail.com",
            "contrasenya": "12345"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Inici de sessió exitós", response.json.get("missatge"))
    
    # Test para obtener un usuario por correo
    def test_obtenir_usuari_per_correu(self):
        response = self.client.post('/iniciar_sessio', json={
            "correu": "prova@gmail.com",
            "contrasenya": "12345"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("usuari")["nom_usuari"], "mare")

    # Test para obtener un niño por ID
    def test_obtenir_nen_per_id(self):
        response = self.client.get('/nen/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("nom"), "Pep")
    
    # Test para la creación de un "tap"
    def test_crear_tap(self):
        response = self.client.post('/tap', json={
            "nen_id": 1,
            "data": "2024-12-18",
            "hora": "19:42:43",
            "estat": "dormint",
            "hores_totals": 1.0
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("Tap creat amb èxit", response.json.get("missatge"))
    
    # Test para obtener el historial de taps de un niño
    def test_obtenir_historial_taps(self):
        response = self.client.get('/tap/historial/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)  # Esperamos 1 tap para el nen con id 1

    # Test para la creación de un niño
    def test_crear_nen(self):
        response = self.client.post('/nen', json={
            "usuari_id": 1,
            "nom": "Anna",
            "data_naixement": "2017-06-10",
            "informacio_medica": "Cap"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("Nen creat amb èxit", response.json.get("missatge"))

    # Test para intentar crear un tap con error (por ejemplo, sin datos completos)
    def test_crear_tap_error(self):
        response = self.client.post('/tap', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Error en crear el tap", response.json.get("error"))

if __name__ == '__main__':
    unittest.main()
