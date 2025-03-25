import requests
import jwt
import os
import json
from datetime import datetime
from datetime import timedelta

# Clase para gestión de tokens (nueva)
class AuthManager:
    def __init__(self):
        self.token_file = 'auth_token.json'
        self.token = None
        self.usuari = None
        self.carregar_token()
    
    def carregar_token(self):
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as f:
                data = json.load(f)
                self.token = data.get('token')
                self.usuari = data.get('usuari')
    
    def guardar_token(self, token, usuari):
        self.token = token
        self.usuari = usuari
        with open(self.token_file, 'w') as f:
            json.dump({'token': token, 'usuari': usuari}, f)
    
    def eliminar_token(self):
        if os.path.exists(self.token_file):
            os.remove(self.token_file)
        self.token = None
        self.usuari = None
    
    def token_valido(self):
        if not self.token:
            return False
        
        try:
            resposta = requests.post(
                "http://127.0.0.1:5000/verificar_token",
                json={"token": self.token}
            )
            return resposta.status_code == 200
        except:
            return False

# Modelos (igual que prototipo 2)
class Usuari:
    def __init__(self, id, nom_usuari, correu, contrasenya, nom, cognom):
        self.id = id
        self.nom_usuari = nom_usuari
        self.correu = correu
        self.contrasenya = contrasenya
        self.nom = nom
        self.cognom = cognom

    def __str__(self):
        return (f"Id: {self.id}, Nom d'usuari: {self.nom_usuari}, Correu: {self.correu}, "
                f"Nom: {self.nom} {self.cognom}")

class Nen:
    def __init__(self, id, usuari_id, nom, data_naixement, informacio_medica):
        self.id = id
        self.usuari_id = usuari_id
        self.nom = nom
        self.data_naixement = data_naixement
        self.informacio_medica = informacio_medica

    def __str__(self):
        return (f"Id: {self.id}, Nom: {self.nom}, "
                f"Data de Naixement: {self.data_naixement}, "
                f"Informació Mèdica: {self.informacio_medica}")

class Tap:
    def __init__(self, id, nen_id, data, hora, estat, hores_totals):
        self.id = id
        self.nen_id = nen_id
        self.data = data
        self.hora = hora
        self.estat = estat
        self.hores_totals = hores_totals

    def __str__(self):
        return (f"Id: {self.id}, Data: {self.data}, Hora: {self.hora}, "
                f"Estat: {self.estat}, Hores Totals: {self.hores_totals}")

class Error:
    def __init__(self, codi_error, descripcio):
        self.codi_error = codi_error
        self.descripcio = descripcio

    def __str__(self):
        return f"Error {self.codi_error}: {self.descripcio}"

# DAOs (igual que prototipo 2 pero con gestión de token)
class DaoUsuari:
    def __init__(self, auth_manager):
        self.base_url = "http://127.0.0.1:5000"
        self.auth_manager = auth_manager
    
    def obtenir_usuari_per_correu(self, correu, contrasenya):
        try:
            resposta = requests.post(
                f"{self.base_url}/iniciar_sessio",
                json={"correu": correu, "contrasenya": contrasenya}
            )

            if resposta.status_code == 200:
                dades = resposta.json()
                self.auth_manager.guardar_token(dades['token'], dades['usuari'])
                return Usuari(
                    dades['usuari']['id'],
                    dades['usuari']['nom_usuari'],
                    dades['usuari']['correu'],
                    dades['usuari']['contrasenya'],
                    dades['usuari']['nom'],
                    dades['usuari']['cognom']
                )
            return Error(resposta.status_code, resposta.json().get('error', 'Error desconegut'))
        except requests.exceptions.RequestException as e:
            return Error(500, f"Error de connexió: {str(e)}")

class DaoNen:
    def __init__(self, auth_manager):
        self.base_url = "http://127.0.0.1:5000"
        self.auth_manager = auth_manager

    def obtenir_nen_per_id(self, nen_id):
        try:
            headers = {'Authorization': f'Bearer {self.auth_manager.token}'} if self.auth_manager.token else {}
            
            resposta = requests.get(
                f"{self.base_url}/nen/{nen_id}",
                headers=headers
            )

            if resposta.status_code == 200:
                dades = resposta.json()
                return Nen(
                    dades['id'],
                    dades['usuari_id'],
                    dades['nom'],
                    dades['data_naixement'],
                    dades['informacio_medica']
                )
            return Error(resposta.status_code, resposta.json().get('error', 'Error desconegut'))
        except requests.exceptions.RequestException as e:
            return Error(500, f"Error de connexió: {str(e)}")

class DaoTap:
    def __init__(self, auth_manager):
        self.base_url = "http://127.0.0.1:5000"
        self.auth_manager = auth_manager

    def obtenir_historial_taps(self, nen_id):
        try:
            headers = {'Authorization': f'Bearer {self.auth_manager.token}'} if self.auth_manager.token else {}
            
            resposta = requests.get(
                f"{self.base_url}/tap/historial/{nen_id}",
                headers=headers
            )

            if resposta.status_code == 200:
                return [Tap(
                    t['id'],
                    t['nen_id'],
                    t['data'],
                    t['hora'],
                    t['estat'],
                    t['hores_totals']
                ) for t in resposta.json()]
            return Error(resposta.status_code, resposta.json().get('error', 'Error desconegut'))
        except requests.exceptions.RequestException as e:
            return Error(500, f"Error de connexió: {str(e)}")

# Vista (igual que prototipo 2 pero con gestión de autenticación)
class Vista:
    def __init__(self, auth_manager):
        self.auth_manager = auth_manager
    
    def mostrar_menu_principal(self):
        print("\n--- Menú Principal ---")
        if self.auth_manager.token_valido():
            print(f"Benvingut/da, {self.auth_manager.usuari['nom']}!")
            print("1. Veure informació del nen")
            print("2. Veure historial de taps")
            print("3. Tancar sessió")
        else:
            print("1. Iniciar sessió")
            print("2. Sortir")
    
    def obtenir_opcio(self):
        return input("Selecciona una opció: ").strip()
    
    def obtenir_credencials(self):
        correu = input("Introdueix el teu correu: ").strip()
        contrasenya = input("Introdueix la teva contrasenya: ").strip()
        return correu, contrasenya
    
    def mostrar_info_usuari(self, usuari):
        if isinstance(usuari, Usuari):
            print(f"\nInformació de l'usuari:\n{usuari}")
        else:
            print("\nNo s'ha pogut obtenir la informació de l'usuari.")
    
    def mostrar_info_nen(self, nen):
        if isinstance(nen, Nen):
            print(f"\nInformació del nen:\n{nen}")
        else:
            print("\nNo s'ha pogut obtenir la informació del nen.")
    
    def mostrar_historial_taps(self, historial_taps):
        if isinstance(historial_taps, list):
            print("\nHistorial de taps:")
            for tap in historial_taps:
                print(tap)
        else:
            print("\nNo s'ha pogut obtenir l'historial de taps.")
    
    def obtenir_id_nen(self):
        return input("Introdueix l'ID del nen: ").strip()
    
    def mostrar_missatge(self, missatge):
        print(f"\n{missatge}")

# Controlador (igual funcionalidad pero con gestión de token)
class Controlador:
    def __init__(self):
        self.auth_manager = AuthManager()
        self.vista = Vista(self.auth_manager)
        self.dao_usuari = DaoUsuari(self.auth_manager)
        self.dao_nen = DaoNen(self.auth_manager)
        self.dao_tap = DaoTap(self.auth_manager)
    
    def executar(self):
        while True:
            self.vista.mostrar_menu_principal()
            opcio = self.vista.obtenir_opcio()
            
            if self.auth_manager.token_valido():
                if opcio == '1':
                    self.mostrar_info_nen()
                elif opcio == '2':
                    self.mostrar_historial_taps()
                elif opcio == '3':
                    self.auth_manager.eliminar_token()
                    self.vista.mostrar_missatge("Sessió tancada correctament.")
                else:
                    self.vista.mostrar_missatge("Opció no vàlida")
            else:
                if opcio == '1':
                    self.iniciar_sessio()
                elif opcio == '2':
                    self.vista.mostrar_missatge("Fins aviat!")
                    break
                else:
                    self.vista.mostrar_missatge("Opció no vàlida")
    
    def iniciar_sessio(self):
        correu, contrasenya = self.vista.obtenir_credencials()
        resultat = self.dao_usuari.obtenir_usuari_per_correu(correu, contrasenya)
        self.vista.mostrar_info_usuari(resultat)
    
    def mostrar_info_nen(self):
        nen_id = self.vista.obtenir_id_nen()
        resultat = self.dao_nen.obtenir_nen_per_id(nen_id)
        self.vista.mostrar_info_nen(resultat)
    
    def mostrar_historial_taps(self):
        nen_id = self.vista.obtenir_id_nen()
        resultat = self.dao_tap.obtenir_historial_taps(nen_id)
        self.vista.mostrar_historial_taps(resultat)

if __name__ == "__main__":
    controlador = Controlador()
    controlador.executar()