from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import jwt
from functools import wraps
from flask_cors import CORS
import logging
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# ----------------------------
# CONFIGURACIÓN INICIAL
# ----------------------------
load_dotenv()
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clau_secreta_per_defecte')
logging.basicConfig(level=logging.INFO)

# ----------------------------
# CONEXIÓN A LA BASE DE DATOS
# ----------------------------
class DBConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBConnection, cls).__new__(cls)
            cls._instance.connection = None
            cls._instance.connect()
        return cls._instance
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                database=os.getenv('DB_NAME', 'TapatApp'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', 'root'),
            )
            if self.connection.is_connected():
                logging.info("✅ Conexión a MySQL establecida")
        except Error as e:
            logging.error(f"❌ Error al conectar a MySQL: {e}")
    
    def get_connection(self):
        if not self.connection.is_connected():
            self.connect()
        return self.connection
    
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logging.info("🔌 Conexión MySQL cerrada")

# ----------------------------
# MODELOS DE DATOS
# ----------------------------
class Usuario:
    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

class Nen:
    def __init__(self, id, child_name, sleep_average, treatment_id, time):
        self.id = id
        self.child_name = child_name
        self.sleep_average = sleep_average
        self.treatment_id = treatment_id
        self.time = time
    
    def to_dict(self):
        return {
            'id': self.id,
            'child_name': self.child_name,
            'sleep_average': self.sleep_average,
            'treatment_id': self.treatment_id,
            'time': self.time
        }

class Tap:
    def __init__(self, id, child_id, status_id, user_id, init, end=None):
        self.id = id
        self.child_id = child_id
        self.status_id = status_id
        self.user_id = user_id
        self.init = init
        self.end = end
    
    def to_dict(self):
        return {
            'id': self.id,
            'child_id': self.child_id,
            'status_id': self.status_id,
            'user_id': self.user_id,
            'init': self.init.isoformat() if self.init else None,
            'end': self.end.isoformat() if self.end else None
        }

# ----------------------------
# ACCESO A DATOS (DAOs)
# ----------------------------
class DAOUsuarios:
    def __init__(self):
        self.db = DBConnection()
    
    def obtener_por_credenciales(self, username, password):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT u.*, r.type_rol as rol 
                FROM User u
                JOIN RelationUserChild ruc ON u.id = ruc.user_id
                JOIN Rol r ON ruc.rol_id = r.id
                WHERE u.username = %s AND u.password = %s
            """
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            
            if result:
                # Obtener todos los roles del usuario
                cursor.execute("""
                    SELECT r.type_rol 
                    FROM RelationUserChild ruc
                    JOIN Rol r ON ruc.rol_id = r.id
                    WHERE ruc.user_id = %s
                """, (result['id'],))
                roles = [row['type_rol'] for row in cursor.fetchall()]
                
                return Usuario(**result), roles
            return None, None
        except Error as e:
            logging.error(f"Error en DAOUsuarios.obtener_por_credenciales: {e}")
            return None, None
        finally:
            if 'cursor' in locals():
                cursor.close()

class DAONens:
    def __init__(self):
        self.db = DBConnection()
    
    def obtener_por_usuario(self, user_id):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT c.* FROM Child c
                JOIN RelationUserChild ruc ON c.id = ruc.child_id
                WHERE ruc.user_id = %s
            """
            cursor.execute(query, (user_id,))
            
            return [Nen(**row) for row in cursor.fetchall()]
        except Error as e:
            logging.error(f"Error en DAONens.obtener_por_usuario: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()

class DAOTaps:
    def __init__(self):
        self.db = DBConnection()
    
    def obtener_por_nen(self, child_id, fecha=None):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            if fecha:
                query = """
                    SELECT * FROM Tap 
                    WHERE child_id = %s AND DATE(init) = STR_TO_DATE(%s, '%%d-%%m-%%Y')
                    ORDER BY init DESC
                """
                cursor.execute(query, (child_id, fecha))
            else:
                query = """
                    SELECT * FROM Tap 
                    WHERE child_id = %s
                    ORDER BY init DESC
                """
                cursor.execute(query, (child_id,))
            
            taps = []
            for row in cursor.fetchall():
                row['init'] = row['init'].replace(tzinfo=None)  # Elimina timezone si existe
                if row.get('end'):
                    row['end'] = row['end'].replace(tzinfo=None)
                taps.append(Tap(**row))
            
            return taps
        except Error as e:
            logging.error(f"Error en DAOTaps.obtener_por_nen: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()

# ----------------------------
# DECORADORES
# ----------------------------
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Obtener token del header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({
                "coderesponse": "0",
                "msg": "Token requerido"
            }), 401
        
        try:
            # Decodificar token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data
        except jwt.ExpiredSignatureError:
            return jsonify({
                "coderesponse": "0",
                "msg": "Token expirado"
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                "coderesponse": "0",
                "msg": "Token inválido"
            }), 401
        except Exception as e:
            return jsonify({
                "coderesponse": "0",
                "msg": f"Error: {str(e)}"
            }), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

# ----------------------------
# SERVICIO WEB
# ----------------------------
servicio_web = type('ServicioWeb', (), {
    'usuarios': DAOUsuarios(),
    'nens': DAONens(),
    'taps': DAOTaps()
})

# ----------------------------
# ENDPOINTS
# ----------------------------
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({
                "coderesponse": "0",
                "msg": "No validat"
            }), 400
        
        usuario, roles = servicio_web.usuarios.obtener_por_credenciales(
            data['username'], data['password'])
        
        if not usuario:
            return jsonify({
                "coderesponse": "0",
                "msg": "No validat"
            }), 401
        
        token_payload = {
            'user_id': usuario.id,
            'username': usuario.username,
            'roles': roles,
            'exp': datetime.utcnow() + timedelta(days=7)
        }
        token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({
            "coderesponse": "1",
            "msg": "Usuari Ok",
            "id": usuario.id,
            "username": usuario.username,
            "email": usuario.email,
            "token": token,
            "idrole": roles[0] if roles else None
        }), 200
    
    except Exception as e:
        logging.error(f"Error en endpoint /login: {e}")
        return jsonify({
            "coderesponse": "0",
            "msg": "Error intern del servidor"
        }), 500

@app.route('/child', methods=['POST'])
@token_required
def obtener_nens(current_user):
    try:
        data = request.get_json()
        user_id = data.get('iduser', current_user['user_id'])
        
        nens = servicio_web.nens.obtener_por_usuario(user_id)
        
        return jsonify({
            "coderesponse": "1",
            "msg": str(len(nens)),
            "data": [nen.to_dict() for nen in nens]
        }), 200
    
    except Exception as e:
        logging.error(f"Error en endpoint /child: {e}")
        return jsonify({
            "coderesponse": "0",
            "msg": "Error al obtenir nens"
        }), 500

@app.route('/taps', methods=['POST'])
@token_required
def obtener_taps(current_user):
    try:
        data = request.get_json()
        
        if 'idchild' not in data:
            return jsonify({
                "coderesponse": "0",
                "msg": "ID de nen requerit"
            }), 400
        
        taps = servicio_web.taps.obtener_por_nen(
            data['idchild'], 
            data.get('data'))
        
        return jsonify({
            "coderesponse": "1",
            "msg": str(len(taps)),
            "data": [tap.to_dict() for tap in taps]
        }), 200
    
    except Exception as e:
        logging.error(f"Error en endpoint /taps: {e}")
        return jsonify({
            "coderesponse": "0",
            "msg": "Error al obtenir taps"
        }), 500

# ----------------------------
# INICIO DE LA APLICACIÓN
# ----------------------------
if __name__ == '__main__':
    try:
        # Verificar conexión a la base de datos al iniciar
        db = DBConnection()
        if db.get_connection().is_connected():
            logging.info("🚀 Iniciando servidor Flask...")
            app.run(host='0.0.0.0', port=5000, debug=True)
        else:
            logging.error("No se pudo conectar a la base de datos")
    except KeyboardInterrupt:
        logging.info("🛑 Deteniendo servidor...")
        db.close()
    except Exception as e:
        logging.error(f"Error crítico: {e}")
        db.close()