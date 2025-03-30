from flask import Flask, request, jsonify
from datetime import date

app = Flask(__name__)

# Model de dades
class Usuari:
    def __init__(self, id, nom_usuari, contrasenya, correu, nom, cognom):
        self.id = id
        self.nom_usuari = nom_usuari
        self.contrasenya = contrasenya
        self.correu = correu
        self.nom = nom
        self.cognom = cognom
    
    def a_diccionari(self):
        return self.__dict__

class Nen:
    def __init__(self, id, usuari_id, nom, data_naixement, informacio_medica):
        self.id = id
        self.usuari_id = usuari_id
        self.nom = nom
        self.data_naixement = data_naixement
        self.informacio_medica = informacio_medica
    
    def a_diccionari(self):
        return self.__dict__

class Tap:
    def __init__(self, id, nen_id, data, hora, estat, hores_totals):
        self.id = id
        self.nen_id = nen_id
        self.data = data
        self.hora = hora
        self.estat = estat
        self.hores_totals = hores_totals
    
    def a_diccionari(self):
        return self.__dict__

# Llistes de dades
usuaris = [
    Usuari(id=1, nom_usuari="mare", contrasenya="12345", correu="prova@gmail.com", nom="Mare", cognom="Prova"),
    Usuari(id=2, nom_usuari="pare", contrasenya="123", correu="prova2@gmail.com", nom="Pare", cognom="Prova")
]

nens = [
    Nen(id=1, usuari_id=1, nom="Pep", data_naixement="2015-03-15", informacio_medica="Cap"),
    Nen(id=2, usuari_id=2, nom="Julieta", data_naixement="2018-07-22", informacio_medica="Al·lèrgia als fruits secs")
]

taps = [
    Tap(id=1, nen_id=1, data="2024-12-18", hora="19:42:43", estat="dormint", hores_totals=1.0),
    Tap(id=2, nen_id=2, data="2024-12-18", hora="21:42:43", estat="despert", hores_totals=0.5)
]

# DAO (Objecte d'Accés a Dades)
class DAOUsuaris:
    def __init__(self):
        self.usuaris = usuaris  # Inicialitzar amb la llista d'usuaris
    
    def obtenir_usuari_per_id(self, id):
        return next((u for u in self.usuaris if u.id == id), None)
    
    def obtenir_usuari_per_correu(self, correu):
        return next((u for u in self.usuaris if u.correu == correu), None)
    
    def crear_usuari(self, usuari):
        self.usuaris.append(usuari)
        return True
    
    def actualitzar_usuari(self, usuari):
        usuari_existent = self.obtenir_usuari_per_id(usuari.id)
        if usuari_existent:
            usuari_existent.nom_usuari = usuari.nom_usuari
            usuari_existent.contrasenya = usuari.contrasenya
            usuari_existent.correu = usuari.correu
            usuari_existent.nom = usuari.nom
            usuari_existent.cognom = usuari.cognom
            return True
        return False

class DAONens:
    def __init__(self):
        self.nens = nens  # Inicialitzar amb la llista de nens
    
    def obtenir_nen_per_id(self, nen_id):
        return next((n for n in self.nens if n.id == nen_id), None)
    
    def crear_nen(self, nen):
        self.nens.append(nen)
        return True
    
    def actualitzar_nen(self, nen):
        nen_existent = self.obtenir_nen_per_id(nen.id)
        if nen_existent:
            nen_existent.nom = nen.nom
            nen_existent.data_naixement = nen.data_naixement
            nen_existent.informacio_medica = nen.informacio_medica
            return True
        return False

class DAOTaps:
    def __init__(self):
        self.taps = taps  # Inicialitzar amb la llista de taps
    
    def obtenir_historial_taps(self, nen_id):
        return [tap.a_diccionari() for tap in self.taps if tap.nen_id == nen_id]
    
    def crear_tap(self, tap):
        self.taps.append(tap)
        return True
    
    def actualitzar_tap(self, tap):
        tap_existent = next((t for t in self.taps if t.id == tap.id), None)
        if tap_existent:
            tap_existent.estat = tap.estat
            tap_existent.hores_totals = tap.hores_totals
            return True
        return False

# Servei Web
class ServeiWeb:
    def __init__(self):
        self.dao_usuaris = DAOUsuaris()
        self.dao_nens = DAONens()
        self.dao_taps = DAOTaps()

    def obtenir_usuari_per_correu(self, correu):
        usuari = self.dao_usuaris.obtenir_usuari_per_correu(correu)
        return usuari.a_diccionari() if usuari else None

    def obtenir_nen_per_id(self, nen_id):
        nen = self.dao_nens.obtenir_nen_per_id(nen_id)
        return nen.a_diccionari() if nen else None

    def obtenir_historial_taps(self, nen_id):
        return self.dao_taps.obtenir_historial_taps(nen_id)

    def crear_usuari(self, usuari):
        return self.dao_usuaris.crear_usuari(usuari)

    def crear_nen(self, nen):
        return self.dao_nens.crear_nen(nen)

    def crear_tap(self, tap):
        return self.dao_taps.crear_tap(tap)

servei_web = ServeiWeb()

# Endpoints
@app.route('/iniciar_sessio', methods=['POST'])
def iniciar_sessio():
    dades = request.json
    usuari = servei_web.obtenir_usuari_per_correu(dades.get('correu'))
    if usuari and usuari['contrasenya'] == dades.get('contrasenya'):
                return jsonify({"missatge": "Inici de sessió exitós", "usuari": usuari}), 200
    return jsonify({"error": "Credencials invàlides"}), 401

@app.route('/usuari', methods=['POST'])
def crear_usuari():
    dades = request.json
    nou_usuari = Usuari(
        id=len(usuaris) + 1,
        nom_usuari=dades.get('nom_usuari'),
        contrasenya=dades.get('contrasenya'),
        correu=dades.get('correu'),
        nom=dades.get('nom'),
        cognom=dades.get('cognom')
    )
    if servei_web.crear_usuari(nou_usuari):
        return jsonify({"missatge": "Usuari creat amb èxit", "usuari": nou_usuari.a_diccionari()}), 201
    return jsonify({"error": "Error en crear l'usuari"}), 400

@app.route('/nen', methods=['POST'])
def crear_nen():
    dades = request.json
    nou_nen = Nen(
        id=len(nens) + 1,
        usuari_id=dades.get('usuari_id'),
        nom=dades.get('nom'),
        data_naixement=dades.get('data_naixement'),
        informacio_medica=dades.get('informacio_medica')
    )
    if servei_web.crear_nen(nou_nen):
        return jsonify({"missatge": "Nen creat amb èxit", "nen": nou_nen.a_diccionari()}), 201
    return jsonify({"error": "Error en crear el nen"}), 400

@app.route('/tap', methods=['POST'])
def crear_tap():
    dades = request.json
    nou_tap = Tap(
        id=len(taps) + 1,
        nen_id=dades.get('nen_id'),
        data=dades.get('data'),
        hora=dades.get('hora'),
        estat=dades.get('estat'),
        hores_totals=dades.get('hores_totals')
    )
    if servei_web.crear_tap(nou_tap):
        return jsonify({"missatge": "Tap creat amb èxit", "tap": nou_tap.a_diccionari()}), 201
    return jsonify({"error": "Error en crear el tap"}), 400

@app.route('/nen/<int:nen_id>', methods=['GET'])
def obtenir_nen(nen_id):
    nen = servei_web.obtenir_nen_per_id(nen_id)
    if nen:
        return jsonify(nen), 200
    return jsonify({"error": "Nen no trobat"}), 404

@app.route('/tap/historial/<int:nen_id>', methods=['GET'])
def obtenir_historial_taps(nen_id):
    historial = servei_web.obtenir_historial_taps(nen_id)
    return jsonify(historial), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
