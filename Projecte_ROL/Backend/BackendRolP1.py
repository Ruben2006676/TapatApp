from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, 
    get_jwt_identity, create_refresh_token
)
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import json
from werkzeug.security import generate_password_hash, check_password_hash

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

# ---- Modelos ----
class User:
    @staticmethod
    def create(username, password, role='player'):
        conn = get_db()
        if not conn:
            return None
            
        cursor = conn.cursor(dictionary=True)
        try:
            hashed_pw = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                (username, hashed_pw, role)
            )
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            conn.rollback()
            print(f"Error al crear usuario: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_username(username):
        conn = get_db()
        if not conn:
            return None
            
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error al obtener usuario: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

class Character:
    @staticmethod
    def create(user_id, name, race, char_class, background=""):
        conn = get_db()
        if not conn:
            return None
            
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                INSERT INTO characters (
                    user_id, name, race, class, level, experience,
                    strength, dexterity, constitution, intelligence, wisdom, charisma,
                    hit_points, max_hit_points, gold, background
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                user_id, name, race, char_class,
                1, 0,  # level, experience
                10, 10, 10, 10, 10, 10,  # stats
                10, 10, 0, background  # hp, gold, background
            ))
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            conn.rollback()
            print(f"Error al crear personaje: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_user(user_id):
        conn = get_db()
        if not conn:
            return []
            
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT id, name, race, class, level 
                FROM characters 
                WHERE user_id = %s
            """, (user_id,))
            return cursor.fetchall()
        except Error as e:
            print(f"Error al obtener personajes: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_detail(character_id, user_id):
        conn = get_db()
        if not conn:
            return None
            
        cursor = conn.cursor(dictionary=True)
        try:
            # Verificar que el personaje pertenece al usuario
            cursor.execute("""
                SELECT user_id FROM characters 
                WHERE id = %s
            """, (character_id,))
            owner = cursor.fetchone()
            
            if not owner or owner['user_id'] != user_id:
                return None
            
            # Obtener detalles del personaje
            cursor.execute("""
                SELECT * FROM characters 
                WHERE id = %s
            """, (character_id,))
            character = cursor.fetchone()
            
            if not character:
                return None
                
            # Obtener items, habilidades y hechizos
            cursor.execute("""
                SELECT i.*, ci.quantity, ci.is_equipped 
                FROM character_items ci
                JOIN items i ON ci.item_id = i.id
                WHERE ci.character_id = %s
            """, (character_id,))
            character['items'] = cursor.fetchall()
            
            cursor.execute("""
                SELECT s.*, cs.proficiency_bonus 
                FROM character_skills cs
                JOIN skills s ON cs.skill_id = s.id
                WHERE cs.character_id = %s
            """, (character_id,))
            character['skills'] = cursor.fetchall()
            
            cursor.execute("""
                SELECT sp.*, cs.prepared 
                FROM character_spells cs
                JOIN spells sp ON cs.spell_id = sp.id
                WHERE cs.character_id = %s
            """, (character_id,))
            character['spells'] = cursor.fetchall()
            
            return character
        except Error as e:
            print(f"Error al obtener detalles del personaje: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

# ---- Autenticación ----
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Se requieren username y password'}), 400
    
    if User.get_by_username(data['username']):
        return jsonify({'error': 'El usuario ya existe'}), 400
    
    user_id = User.create(data['username'], data['password'])
    if not user_id:
        return jsonify({'error': 'Error al crear usuario'}), 500
        
    return jsonify({'message': 'Usuario creado exitosamente', 'user_id': user_id}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Se requieren username y password'}), 400
    
    user = User.get_by_username(data['username'])
    if not user or not check_password_hash(user['password'], data['password']):
        return jsonify({'error': 'Credenciales inválidas'}), 401
    
    access_token = create_access_token(identity=user['id'])
    refresh_token = create_refresh_token(identity=user['id'])
    
    characters = Character.get_by_user(user['id'])
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'role': user['role'],
            'characters': characters
        }
    }), 200

# ---- Gestión de Personajes ----
@app.route('/characters', methods=['POST'])
@jwt_required()
def create_character():
    data = request.json
    user_id = get_jwt_identity()
    
    required_fields = ['name', 'race', 'class']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Faltan campos requeridos: name, race, class'}), 400
    
    if not all(data[field] for field in required_fields):
        return jsonify({'error': 'Los campos name, race y class no pueden estar vacíos'}), 400
    
    character_id = Character.create(
        user_id,
        data['name'],
        data['race'],
        data['class'],
        data.get('background', '')
    )
    
    if not character_id:
        return jsonify({'error': 'Error al crear personaje'}), 500
        
    character = Character.get_detail(character_id, user_id)
    if not character:
        return jsonify({'error': 'Error al obtener detalles del personaje'}), 500
    
    return jsonify({
        'message': 'Personaje creado exitosamente',
        'character': character
    }), 201

@app.route('/characters', methods=['GET'])
@jwt_required()
def get_characters():
    user_id = get_jwt_identity()
    characters = Character.get_by_user(user_id)
    return jsonify({'characters': characters}), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
@jwt_required()
def get_character_detail(character_id):
    user_id = get_jwt_identity()
    character = Character.get_detail(character_id, user_id)
    
    if not character:
        return jsonify({'error': 'Personaje no encontrado o no tienes permisos'}), 404
    
    return jsonify(character), 200

if __name__ == '__main__':
    app.run(debug=True)