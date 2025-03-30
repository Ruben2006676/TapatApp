from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import jwt
from functools import wraps
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'clave_secreta_super_segura_para_jwt'

# --- MODELOS ---
class Usuari:
    def __init__(self, id, nom_usuari, contrasenya, correu, nom, cognom, rol):
        self.id = id
        self.nom_usuari = nom_usuari
        self.contrasenya = contrasenya
        self.correu = correu
        self.nom = nom
        self.cognom = cognom
        self.rol = rol

    def a_diccionari(self):
        return {k: v for k, v in self.__dict__.items() if k != 'contrasenya'}

class Nen:
    def __init__(self, id, tutor_id, cuidador_id, nom, data_naixement, informacio_medica):
        self.id = id
        self.tutor_id = tutor_id
        self.cuidador_id = cuidador_id
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

# --- DATOS DE EJEMPLO ---
usuaris = [
    Usuari(id=1, nom_usuari="mare", contrasenya="123", correu="mare@exemple.com", nom="Maria", cognom="Garcia", rol="tutor"),
    Usuari(id=2, nom_usuari="pare", contrasenya="123", correu="pare@exemple.com", nom="Pere", cognom="Martinez", rol="tutor"),
    Usuari(id=3, nom_usuari="cuidador1", contrasenya="123", correu="cuidador1@exemple.com", nom="Anna", cognom="Lopez", rol="cuidador")
]

nens = [
    Nen(id=1, tutor_id=1, cuidador_id=3, nom="Pep", data_naixement="2015-03-15", informacio_medica="Cap"),
    Nen(id=2, tutor_id=2, cuidador_id=3, nom="Julieta", data_naixement="2018-07-22", informacio_medica="Al·lèrgia als fruits secs")
]

taps = [
    Tap(id=1, nen_id=1, data="2024-12-18", hora="19:42:43", estat="dormint", hores_totals=1.0),
    Tap(id=2, nen_id=2, data="2024-12-18", hora="21:42:43", estat="despert", hores_totals=0.5)
]

# --- DAOs ---
class DAOUsuaris:
    def __init__(self):
        self.usuaris = usuaris
    
    def obtenir_usuari_per_id(self, id):
        return next((u for u in self.usuaris if u.id == id), None)
    
    def obtenir_usuari_per_correu(self, correu):
        for u in self.usuaris:
            if u.correu == correu:
                return u
        return None
    
    def obtenir_nens_per_usuari(self, usuari_id, rol):
        if rol == 'tutor':
            return [n for n in nens if n.tutor_id == usuari_id]
        elif rol == 'cuidador':
            return [n for n in nens if n.cuidador_id == usuari_id]
        return []
    
    def crear_usuari(self, usuari):
        self.usuaris.append(usuari)
        return True
    
    def actualitzar_usuari(self, usuari):
        usuari_existent = self.obtenir_usuari_per_id(usuari.id)
        if usuari_existent:
            for key, value in usuari.__dict__.items():
                setattr(usuari_existent, key, value)
            return True
        return False

class DAONens:
    def __init__(self):
        self.nens = nens
    
    def obtenir_nen_per_id(self, nen_id):
        return next((n for n in self.nens if n.id == nen_id), None)
    
    def obtenir_nens_per_rol(self, usuari_id, rol):
        if rol == 'tutor':
            return [n for n in self.nens if n.tutor_id == usuari_id]
        elif rol == 'cuidador':
            return [n for n in self.nens if n.cuidador_id == usuari_id]
        return []
    
    def crear_nen(self, nen):
        self.nens.append(nen)
        return True
    
    def actualitzar_nen(self, nen):
        nen_existent = self.obtenir_nen_per_id(nen.id)
        if nen_existent:
            for key, value in nen.__dict__.items():
                setattr(nen_existent, key, value)
            return True
        return False

class DAOTaps:
    def __init__(self):
        self.taps = taps
    
    def obtenir_tap_per_id(self, tap_id):
        return next((t for t in self.taps if t.id == tap_id), None)
    
    def obtenir_taps_per_nen(self, nen_id):
        return [t for t in self.taps if t.nen_id == nen_id]
    
    def obtenir_taps_per_usuari(self, usuari_id, rol):
        nens_dao = DAONens()
        nens_usuario = nens_dao.obtenir_nens_per_rol(usuari_id, rol)
        taps = []
        for nen in nens_usuario:
            taps.extend(self.obtenir_taps_per_nen(nen.id))
        return taps
    
    def crear_tap(self, tap):
        self.taps.append(tap)
        return True
    
    def actualitzar_tap(self, tap):
        tap_existent = self.obtenir_tap_per_id(tap.id)
        if tap_existent:
            for key, value in tap.__dict__.items():
                setattr(tap_existent, key, value)
            return True
        return False

# --- SERVEI WEB ---
class ServeiWeb:
    def __init__(self):
        self.dao_usuaris = DAOUsuaris()
        self.dao_nens = DAONens()
        self.dao_taps = DAOTaps()
    
    def autenticar(self, correu, contrasenya):
        usuari = self.dao_usuaris.obtenir_usuari_per_correu(correu)
        if usuari and hasattr(usuari, 'contrasenya') and usuari.contrasenya == contrasenya:
            return usuari
        return None
    
    def obtenir_info_usuari(self, usuari_id):
        return self.dao_usuaris.obtenir_usuari_per_id(usuari_id)
    
    def obtenir_nens_usuari(self, usuari_id, rol):
        return self.dao_nens.obtenir_nens_per_rol(usuari_id, rol)
    
    def obtenir_taps_usuari(self, usuari_id, rol):
        return self.dao_taps.obtenir_taps_per_usuari(usuari_id, rol)
    
    def crear_usuari(self, usuari):
        return self.dao_usuaris.crear_usuari(usuari)
    
    def actualitzar_usuari(self, usuari):
        return self.dao_usuaris.actualitzar_usuari(usuari)
    
    def crear_nen(self, nen):
        return self.dao_nens.crear_nen(nen)
    
    def actualitzar_nen(self, nen):
        return self.dao_nens.actualitzar_nen(nen)
    
    def crear_tap(self, tap):
        return self.dao_taps.crear_tap(tap)
    
    def actualitzar_tap(self, tap):
        return self.dao_taps.actualitzar_tap(tap)

servei_web = ServeiWeb()

# --- DECORADOR TOKEN REQUIRED ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token faltant'}), 401
            
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = servei_web.obtenir_info_usuari(data['user_id'])
            
            if not current_user:
                return jsonify({'message': 'Usuari no existeix'}), 401
                
            if current_user.rol != data['rol']:
                return jsonify({'message': 'Permisos modificats'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirat'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token invàlid'}), 401
        except Exception as e:
            return jsonify({'message': f'Error: {str(e)}'}), 401
            
        return f(current_user, *args, **kwargs)
        
    return decorated

# --- ENDPOINTS ---
@app.route('/iniciar_sessio', methods=['POST'])
def iniciar_sessio():
    try:
        dades = request.get_json()
        if not dades or 'correu' not in dades or 'contrasenya' not in dades:
            return jsonify({"error": "Correu i contrasenya requerits"}), 400
        
        usuari = servei_web.autenticar(dades['correu'], dades['contrasenya'])
        if not usuari or not hasattr(usuari, 'id'):
            return jsonify({"error": "Credencials invàlides"}), 401
        
        token = jwt.encode({
            'user_id': usuari.id,
            'rol': usuari.rol,
            'nom': usuari.nom,
            'cognom': usuari.cognom,
            'correu': usuari.correu,
            'nom_usuari': usuari.nom_usuari,
            'exp': datetime.utcnow() + timedelta(days=7)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({
            "token": token,
            "usuari": usuari.a_diccionari(),
            "rol": usuari.rol
        }), 200
    except Exception as e:
        return jsonify({"error": f"Error intern: {str(e)}"}), 500

@app.route('/perfil', methods=['GET'])
@token_required
def perfil_usuari(current_user):
    return jsonify(current_user.a_diccionari()), 200

@app.route('/nens', methods=['GET'])
@token_required
def obtenir_nens(current_user):
    nens = servei_web.obtenir_nens_usuari(current_user.id, current_user.rol)
    return jsonify([n.a_diccionari() for n in nens]), 200

@app.route('/taps', methods=['GET'])
@token_required
def obtenir_taps(current_user):
    taps = servei_web.obtenir_taps_usuari(current_user.id, current_user.rol)
    return jsonify([t.a_diccionari() for t in taps]), 200

@app.route('/crear_usuari', methods=['POST'])
def crear_usuari():
    try:
        dades = request.get_json()
        nou_id = max(u.id for u in usuaris) + 1 if usuaris else 1
        nou_usuari = Usuari(
            id=nou_id,
            nom_usuari=dades['nom_usuari'],
            contrasenya=dades['contrasenya'],
            correu=dades['correu'],
            nom=dades['nom'],
            cognom=dades['cognom'],
            rol=dades['rol']
        )
        if servei_web.crear_usuari(nou_usuari):
            return jsonify({"missatge": "Usuari creat correctament", "id": nou_id}), 201
        return jsonify({"error": "Error creant l'usuari"}), 400
    except Exception as e:
        return jsonify({"error": f"Error intern: {str(e)}"}), 500

@app.route('/crear_nen', methods=['POST'])
@token_required
def crear_nen(current_user):
    try:
        dades = request.get_json()
        nou_id = max(n.id for n in nens) + 1 if nens else 1
        nou_nen = Nen(
            id=nou_id,
            tutor_id=dades['tutor_id'],
            cuidador_id=dades['cuidador_id'],
            nom=dades['nom'],
            data_naixement=dades['data_naixement'],
            informacio_medica=dades['informacio_medica']
        )
        if servei_web.crear_nen(nou_nen):
            return jsonify({"missatge": "Nen creat correctament", "id": nou_id}), 201
        return jsonify({"error": "Error creant el nen"}), 400
    except Exception as e:
        return jsonify({"error": f"Error intern: {str(e)}"}), 500

@app.route('/crear_tap', methods=['POST'])
@token_required
def crear_tap(current_user):
    try:
        dades = request.get_json()
        nou_id = max(t.id for t in taps) + 1 if taps else 1
        nou_tap = Tap(
            id=nou_id,
            nen_id=dades['nen_id'],
            data=dades['data'],
            hora=dades['hora'],
            estat=dades['estat'],
            hores_totals=dades['hores_totals']
        )
        if servei_web.crear_tap(nou_tap):
            return jsonify({"missatge": "Tap creat correctament", "id": nou_id}), 201
        return jsonify({"error": "Error creant el tap"}), 400
    except Exception as e:
        return jsonify({"error": f"Error intern: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
