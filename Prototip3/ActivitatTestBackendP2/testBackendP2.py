import unittest
from flask import Flask, jsonify
from flask.testing import FlaskClient
from BackendP2 import app, Usuari, Nen, Tap, ServeiWeb, DAOUsuaris, DAONens, DAOTaps

class TestBackend(unittest.TestCase):

    # Configuración de la aplicación para pruebas
    def setUp(self):
        # Creamos un cliente de pruebas de Flask
        self.app: Flask = app
        self.client: FlaskClient = self.app.test_client()
        self.app.testing = True  # Activar el modo de testing

        # Aquí podrías limpiar la base de datos de prueba si es necesario.
        # Ejemplo: Limpiar todos los taps o usuarios previos para no interferir en las pruebas.
        # DAOUsuaris.borrar_todos()   # Si tu base de datos permite esta operación
        # DAONens.borrar_todos()
        # DAOTaps.borrar_todos()

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
        # Verificamos que al menos 1 tap esté presente
        self.assertGreaterEqual(len(response.json), 1)

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
        # Enviar datos vacíos, lo cual debería resultar en un error
        response = self.client.post('/tap', json={})
        self.assertEqual(response.status_code, 400)  # Error esperado 400 (Bad Request)
        self.assertIn("Error en crear el tap", response.json.get("error"))  # Ajustado al mensaje real

if __name__ == '__main__':
    unittest.main()
