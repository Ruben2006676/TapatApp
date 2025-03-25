from flask import Flask, request, jsonify
from datetime import datetime, timedelta  
import hashlib
import jwt  
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_super_segura_para_jwt'  # En producción usar una clave más segura

# Modelos (exactamente igual que en prototipo 2)
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

# Datos de ejemplo (igual que prototipo 2)
usuaris = [
    Usuari(id=1, nom_usuari="mare", contrasenya="123", correu="prova@gmail.com", nom="Mare", cognom="Prova"),
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

# DAOs (exactamente igual que prototipo 2)
class DAOUsuaris:
    def __init__(self):
        self.usuaris = usuaris
    
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
        self.nens = nens
    
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
        self.taps = taps
    
    def obtenir_tap_per_id(self, tap_id):
        return next((t for t in self.taps if t.id == tap_id), None)
    
    def crear_tap(self, tap):
        self.taps.append(tap)
        return True
    
    def obtenir_historial_taps_per_nen_id(self, nen_id):
        return [t for t in self.taps if t.nen_id == nen_id]

# ServeiWeb (igual que prototipo 2 pero con añadidos JWT)
class ServeiWeb:
    def __init__(self):
        self.dao_usuaris = DAOUsuaris()
        self.dao_nens = DAONens()
        self.dao_taps = DAOTaps()
    
    def obtenir_usuari_per_correu(self, correu):
        usuari = self.dao_usuaris.obtenir_usuari_per_correu(correu)
        return usuari.a_diccionari() if usuari else None
    
    def crear_usuari(self, usuari):
        return self.dao_usuaris.crear_usuari(usuari)
    
    def crear_nen(self, nen):
        return self.dao_nens.crear_nen(nen)
    
    def crear_tap(self, tap):
        return self.dao_taps.crear_tap(tap)
    
    def obtenir_nen_per_id(self, nen_id):
        nen = self.dao_nens.obtenir_nen_per_id(nen_id)
        return nen.a_diccionari() if nen else None
    
    def obtenir_historial_taps_per_nen_id(self, nen_id):
        taps = self.dao_taps.obtenir_historial_taps_per_nen_id(nen_id)
        return [t.a_diccionari() for t in taps]

servei_web = ServeiWeb()

# Decorador para verificar token JWT (nuevo)
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token no proporcionado'}), 401
            
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = servei_web.dao_usuaris.obtenir_usuari_per_id(data['user_id'])
            if not current_user:
                return jsonify({'message': 'Usuario no encontrado'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401
            
        return f(current_user, *args, **kwargs)
        
    return decorated

# Endpoints originales (prototipo 2) + nuevos para JWT
@app.route('/iniciar_sessio', methods=['POST'])
def iniciar_sessio():
    dades = request.json
    usuari = servei_web.obtenir_usuari_per_correu(dades.get('correu'))
    if usuari and usuari['contrasenya'] == dades.get('contrasenya'):
        # Generar token JWT (nuevo)
        token = jwt.encode({
            'user_id': usuari['id'],
            'exp': datetime.utcnow() + timedelta(days=7)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({
            "missatge": "Inici de sessió exitós",
            "usuari": usuari,
            "token": token  # Nuevo
        }), 200
    return jsonify({"error": "Credencials invàlides"}), 401

@app.route('/verificar_token', methods=['POST'])  # Nuevo endpoint
def verificar_token():
    token = request.json.get('token')
    if not token:
        return jsonify({'valid': False, 'message': 'Token no proporcionado'}), 400
        
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        current_user = servei_web.dao_usuaris.obtenir_usuari_per_id(data['user_id'])
        if current_user:
            return jsonify({
                'valid': True,
                'usuari': current_user.a_diccionari(),
                'message': 'Token válido'
            }), 200
        return jsonify({'valid': False, 'message': 'Usuario no encontrado'}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({'valid': False, 'message': 'Token expirado'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'valid': False, 'message': 'Token inválido'}), 401

# Endpoints originales PROTEGIDOS con token (modificados)
@app.route('/usuari', methods=['POST'])
@token_required  # Nuevo
def crear_usuari(current_user):
    dades = request.json
    usuari = Usuari(**dades)
    if servei_web.crear_usuari(usuari):
        return jsonify({"missatge": "Usuari creat correctament"}), 201
    return jsonify({"error": "No s'ha pogut crear l'usuari"}), 400

@app.route('/nen', methods=['POST'])
@token_required  # Nuevo
def crear_nen(current_user):
    dades = request.json
    nen = Nen(**dades)
    if servei_web.crear_nen(nen):
        return jsonify({"missatge": "Nen creat correctament"}), 201
    return jsonify({"error": "No s'ha pogut crear el nen"}), 400

@app.route('/tap', methods=['POST'])
@token_required  # Nuevo
def crear_tap(current_user):
    dades = request.json
    tap = Tap(**dades)
    if servei_web.crear_tap(tap):
        return jsonify({"missatge": "Tap creat correctament"}), 201
    return jsonify({"error": "No s'ha pogut crear el tap"}), 400

@app.route('/nen/<int:nen_id>', methods=['GET'])
@token_required  # Nuevo
def obtenir_nen(current_user, nen_id):
    nen = servei_web.obtenir_nen_per_id(nen_id)
    if nen:
        return jsonify(nen), 200
    return jsonify({"error": "Nen no trobat"}), 404

@app.route('/tap/historial/<int:nen_id>', methods=['GET'])
@token_required  # Nuevo
def obtenir_historial_taps(current_user, nen_id):
    taps = servei_web.obtenir_historial_taps_per_nen_id(nen_id)
    if taps:
        return jsonify(taps), 200
    return jsonify({"error": "No s'han trobat taps per aquest nen"}), 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)