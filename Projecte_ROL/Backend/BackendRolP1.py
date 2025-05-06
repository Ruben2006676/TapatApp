from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, 
    get_jwt_identity, create_refresh_token
)
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'clave_secreta_super_segura'
jwt = JWTManager(app)

# ---- Conexión a BD ----
def get_db():
    try:
        return mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="rolplayer.bd",
            port=3306
        )
    except Error as e:
        print(f"Error de conexión: {e}")
        return None

# ---- Autenticación ----
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT * FROM users 
        WHERE username = %s AND password = %s
    """, (data['username'], data['password']))
    
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user:
        access_token = create_access_token(identity=user['id'])
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user['id'],
                'role': user['role']
            }
        }), 200
    
    return jsonify({'error': 'Credenciales inválidas'}), 401

# ---- Gestión de Personajes ----
@app.route('/characters', methods=['POST'])
@jwt_required()
def create_character():
    data = request.json
    user_id = get_jwt_identity()
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO characters (
                user_id, name, race, class, 
                strength, dexterity, constitution,
                intelligence, wisdom, charisma
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id, data['name'], data['race'], data['class'],
            10, 10, 10, 10, 10, 10  # Valores por defecto
        ))
        
        conn.commit()
        return jsonify({'message': 'Personaje creado'}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/characters', methods=['GET'])
@jwt_required()
def get_characters():
    user_id = get_jwt_identity()
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT * FROM characters 
        WHERE user_id = %s
    """, (user_id,))
    
    characters = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify({
        'characters': [
            {
                'id': c['id'],
                'name': c['name'],
                'race': c['race'],
                'class': c['class'],
                'stats': {
                    'strength': c['strength'],
                    'dexterity': c['dexterity'],
                    'constitution': c['constitution'],
                    'intelligence': c['intelligence'],
                    'wisdom': c['wisdom'],
                    'charisma': c['charisma']
                }
            } for c in characters
        ]
    }), 200

# ---- Gestión de Partidas ----
@app.route('/game_sessions', methods=['POST'])
@jwt_required()
def create_game_session():
    data = request.json
    user_id = get_jwt_identity()
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO game_sessions (
                adventure_id, game_master_id, status
            ) VALUES (%s, %s, 'pending')
        """, (data['adventure_id'], user_id))
        
        conn.commit()
        return jsonify({'message': 'Partida creada'}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/game_sessions/<int:session_id>/join', methods=['POST'])
@jwt_required()
def join_game(session_id):
    data = request.json
    user_id = get_jwt_identity()
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Verificar propiedad del personaje
        cursor.execute("""
            SELECT 1 FROM characters 
            WHERE id = %s AND user_id = %s
        """, (data['character_id'], user_id))
        if not cursor.fetchone():
            return jsonify({'error': 'Personaje no válido'}), 403
        
        # Unir a la partida
        cursor.execute("""
            INSERT INTO session_characters 
            (session_id, character_id) 
            VALUES (%s, %s)
        """, (session_id, data['character_id']))
        
        conn.commit()
        return jsonify({'message': 'Unido a la partida'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# ---- Sistema de Combate ----
@app.route('/combat/<int:session_id>/start', methods=['POST'])
@jwt_required()
def start_combat(session_id):
    user_id = get_jwt_identity()
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Verificar si es el Game Master
        cursor.execute("""
            SELECT 1 FROM game_sessions 
            WHERE id = %s AND game_master_id = %s
        """, (session_id, user_id))
        if not cursor.fetchone():
            return jsonify({'error': 'Acceso no autorizado'}), 403
        
        # Crear encuentro de combate
        cursor.execute("""
            INSERT INTO active_combats 
            (session_id, encounter_id) 
            VALUES (%s, 1)  # Ejemplo con encounter_id fijo
        """, (session_id,))
        
        conn.commit()
        return jsonify({'message': 'Combate iniciado'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# ---- Registro de Acciones ----
@app.route('/game_logs', methods=['POST'])
@jwt_required()
def log_action():
    data = request.json
    user_id = get_jwt_identity()
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO game_logs 
            (session_id, character_id, action_type, description)
            VALUES (%s, %s, %s, %s)
        """, (
            data['session_id'], 
            data.get('character_id'), 
            data['action_type'], 
            data['description']
        ))
        
        conn.commit()
        return jsonify({'message': 'Acción registrada'}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
