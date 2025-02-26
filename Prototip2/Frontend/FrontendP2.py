import requests

# Classe Usuari
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

# Classe Nen
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

# Classe Tap
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

# Classe Error
class Error:
    def __init__(self, codi_error, descripcio):
        self.codi_error = codi_error
        self.descripcio = descripcio

    def __str__(self):
        return f"Error {self.codi_error}: {self.descripcio}"

# Classe DaoUsuari
class DaoUsuari:
    def __init__(self):
        self.base_url = "http://127.0.0.1:5000"

    def obtenir_usuari_per_credencials(self, usuari_id, contrasenya):
        try:
            resposta = requests.post(
                f"{self.base_url}/iniciar_sessio",
                json={"id": usuari_id, "contrasenya": contrasenya}
            )

            if resposta.status_code == 200:
                dades_usuari = resposta.json().get("usuari")
                return Usuari(
                    dades_usuari.get("id"),
                    dades_usuari.get("nom_usuari"),
                    dades_usuari.get("correu"),
                    contrasenya,
                    dades_usuari.get("nom"),
                    dades_usuari.get("cognom")
                )
            else:
                return Error(resposta.status_code, resposta.json().get("error", "Error desconegut"))
        except requests.exceptions.ConnectionError:
            return Error(500, "Error de connexió: No es va poder connectar amb el servidor")
        except requests.exceptions.RequestException as e:
            return Error(500, f"Error inesperat: {str(e)}")

# Classe DaoNen
class DaoNen:
    def __init__(self):
        self.base_url = "http://127.0.0.1:5000"

    def obtenir_nens_per_usuari(self, usuari_id):
        try:
            resposta = requests.get(
                f"{self.base_url}/nen",
                params={"usuari_id": usuari_id}
            )

            if resposta.status_code == 200:
                nens_dades = resposta.json()
                return [Nen(
                    nen.get("id"),
                    nen.get("usuari_id"),
                    nen.get("nom"),
                    nen.get("data_naixement"),
                    nen.get("informacio_medica")
                ) for nen in nens_dades]
            else:
                return Error(resposta.status_code, resposta.json().get("error", "Error desconegut"))
        except requests.exceptions.ConnectionError:
            return Error(500, "Error de connexió: No es va poder connectar amb el servidor")
        except requests.exceptions.RequestException as e:
            return Error(500, f"Error inesperat: {str(e)}")

# Classe DaoTap
class DaoTap:
    def __init__(self):
        self.base_url = "http://127.0.0.1:5000"

    def obtenir_historial_taps_per_usuari(self, usuari_id):
        try:
            resposta = requests.get(
                f"{self.base_url}/tap/historial",
                params={"usuari_id": usuari_id}
            )

            if resposta.status_code == 200:
                taps_dades = resposta.json()
                return [Tap(
                    tap.get("id"),
                    tap.get("nen_id"),
                    tap.get("data"),
                    tap.get("hora"),
                    tap.get("estat"),
                    tap.get("hores_totals")
                ) for tap in taps_dades]
            else:
                return Error(resposta.status_code, resposta.json().get("error", "Error desconegut"))
        except requests.exceptions.ConnectionError:
            return Error(500, "Error de connexió: No es va poder connectar amb el servidor")
        except requests.exceptions.RequestException as e:
            return Error(500, f"Error inesperat: {str(e)}")

# Classe Vista (Consola)
class Vista:
    def obtenir_credencials_per_consola(self):
        usuari_id = int(input("Introdueix l'ID d'usuari: ").strip())
        contrasenya = input("Introdueix la contrasenya: ").strip()
        return usuari_id, contrasenya

    def mostrar_info_usuari(self, usuari):
        if isinstance(usuari, Usuari):
            print(f"\nInformació de l'usuari:\n{usuari}")
        else:
            print("\nNo s'ha pogut obtenir la informació de l'usuari.")

    def mostrar_info_nens(self, nens):
        if isinstance(nens, list):
            print("\nInformació dels nens:")
            for nen in nens:
                print(nen)
        else:
            print("\nNo s'ha pogut obtenir la informació dels nens.")

    def mostrar_historial_taps(self, historial_taps):
        if isinstance(historial_taps, list):
            print("\nHistorial de taps:")
            for tap in historial_taps:
                print(tap)
        else:
            print("\nNo s'ha pogut obtenir l'historial de taps.")

# Funció principal
if __name__ == "__main__":
    vista = Vista()
    dao_usuari = DaoUsuari()
    dao_nen = DaoNen()
    dao_tap = DaoTap()

    usuari_id, contrasenya = vista.obtenir_credencials_per_consola()
    usuari = dao_usuari.obtenir_usuari_per_credencials(usuari_id, contrasenya)
    vista.mostrar_info_usuari(usuari)
