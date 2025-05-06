from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, 
    get_jwt_identity, create_refresh_token
)
import mysql.connector
from mysql.connector import Error
from datetime import datetime

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
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
        
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT * FROM users 
            WHERE username = %s AND password = %s
        """, (data['username'], data['password']))
        
        user = cursor.fetchone()
        
        if user:
            access_token = create_access_token(identity=user['id'])
            refresh_token = create_refresh_token(identity=user['id'])
            
            # Obtener personajes del usuario
            cursor.execute("SELECT id, name, race, class, level FROM characters WHERE user_id = %s", (user['id'],))
            characters = cursor.fetchall()
            
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
        
        return jsonify({'error': 'Credenciales inválidas'}), 401
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ---- Gestión de Personajes ----
@app.route('/characters', methods=['POST'])
@jwt_required()
def create_character():
    data = request.json
    user_id = get_jwt_identity()
    
    # Validación de datos
    required_fields = ['name', 'race', 'class']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Faltan campos requeridos: name, race, class'}), 400
    
    conn = get_db()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
        
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Insertar personaje con valores por defecto
        cursor.execute("""
            INSERT INTO characters (
                user_id, name, race, class, level, experience,
                strength, dexterity, constitution, intelligence, wisdom, charisma,
                hit_points, max_hit_points, gold, background
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id, data['name'], data['race'], data['class'],
            1, 0,  # level, experience
            10, 10, 10, 10, 10, 10,  # stats
            10, 10, 0, data.get('background', '')  # hp, gold, background
        ))
        
        character_id = cursor.lastrowid
        conn.commit()
        
        # Obtener el personaje completo para devolverlo
        cursor.execute("""
            SELECT c.*, 
                   (SELECT COUNT(*) FROM character_items WHERE character_id = c.id) as item_count,
                   (SELECT COUNT(*) FROM character_skills WHERE character_id = c.id) as skill_count,
                   (SELECT COUNT(*) FROM character_spells WHERE character_id = c.id) as spell_count
            FROM characters c 
            WHERE id = %s
        """, (character_id,))
        character = cursor.fetchone()
        
        return jsonify({
            'message': 'Personaje creado exitosamente',
            'character': format_character_response(character)
        }), 201
    except Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()

def format_character_response(character):
    return {
        'id': character['id'],
        'name': character['name'],
        'race': character['race'],
        'class': character['class'],
        'level': character['level'],
        'experience': character['experience'],
        'stats': {
            'strength': character['strength'],
            'dexterity': character['dexterity'],
            'constitution': character['constitution'],
            'intelligence': character['intelligence'],
            'wisdom': character['wisdom'],
            'charisma': character['charisma']
        },
        'health': {
            'current': character['hit_points'],
            'max': character['max_hit_points']
        },
        'gold': character['gold'],
        'background': character['background'],
        'inventory_count': character['item_count'],
        'skills_count': character['skill_count'],
        'spells_count': character['spell_count'],
        'created_at': character['created_at'].isoformat() if character['created_at'] else None
    }

@app.route('/characters', methods=['GET'])
@jwt_required()
def get_characters():
    user_id = get_jwt_identity()
    conn = get_db()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
        
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT c.*, 
                   (SELECT COUNT(*) FROM character_items WHERE character_id = c.id) as item_count,
                   (SELECT COUNT(*) FROM character_skills WHERE character_id = c.id) as skill_count,
                   (SELECT COUNT(*) FROM character_spells WHERE character_id = c.id) as spell_count
            FROM characters c 
            WHERE user_id = %s
        """, (user_id,))
        
        characters = cursor.fetchall()
        
        return jsonify({
            'characters': [format_character_response(c) for c in characters]
        }), 200
    except Error as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/characters/<int:character_id>', methods=['GET'])
@jwt_required()
def get_character_detail(character_id):
    user_id = get_jwt_identity()
    conn = get_db()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
        
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Verificar que el personaje pertenece al usuario
        cursor.execute("SELECT user_id FROM characters WHERE id = %s", (character_id,))
        character_owner = cursor.fetchone()
        
        if not character_owner or character_owner['user_id'] != user_id:
            return jsonify({'error': 'Personaje no encontrado o no tienes permisos'}), 404
        
        # Obtener detalles del personaje
        cursor.execute("""
            SELECT c.*, 
                   (SELECT COUNT(*) FROM character_items WHERE character_id = c.id) as item_count,
                   (SELECT COUNT(*) FROM character_skills WHERE character_id = c.id) as skill_count,
                   (SELECT COUNT(*) FROM character_spells WHERE character_id = c.id) as spell_count
            FROM characters c 
            WHERE id = %s
        """, (character_id,))
        character = cursor.fetchone()
        
        if not character:
            return jsonify({'error': 'Personaje no encontrado'}), 404
        
        # Obtener items del personaje
        cursor.execute("""
            SELECT i.*, ci.quantity, ci.is_equipped 
            FROM character_items ci
            JOIN items i ON ci.item_id = i.id
            WHERE ci.character_id = %s
        """, (character_id,))
        items = cursor.fetchall()
        
        # Obtener habilidades del personaje
        cursor.execute("""
            SELECT s.*, cs.proficiency_bonus 
            FROM character_skills cs
            JOIN skills s ON cs.skill_id = s.id
            WHERE cs.character_id = %s
        """, (character_id,))
        skills = cursor.fetchall()
        
        # Obtener hechizos del personaje
        cursor.execute("""
            SELECT sp.*, cs.prepared 
            FROM character_spells cs
            JOIN spells sp ON cs.spell_id = sp.id
            WHERE cs.character_id = %s
        """, (character_id,))
        spells = cursor.fetchall()
        
        response = format_character_response(character)
        response['items'] = items
        response['skills'] = skills
        response['spells'] = spells
        
        return jsonify(response), 200
    except Error as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# ---- Gestión de Partidas ----
@app.route('/game_sessions', methods=['POST'])
@jwt_required()
def create_game_session():
    data = request.json
    user_id = get_jwt_identity()
    
    if 'adventure_id' not in data:
        return jsonify({'error': 'adventure_id es requerido'}), 400
    
    conn = get_db()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
        
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            INSERT INTO game_sessions (
                adventure_id, game_master_id, status
            ) VALUES (%s, %s, 'pending')
        """, (data['adventure_id'], user_id))
        
        session_id = cursor.lastrowid
        conn.commit()
        
        return jsonify({
            'message': 'Partida creada exitosamente',
            'session_id': session_id
        }), 201
    except Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/game_sessions/<int:session_id>/join', methods=['POST'])
@jwt_required()
def join_game(session_id):
    data = request.json
    user_id = get_jwt_identity()
    
    if 'character_id' not in data:
        return jsonify({'error': 'character_id es requerido'}), 400
    
    conn = get_db()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
        
    cursor = conn.cursor()
    
    try:
        # Verificar propiedad del personaje
        cursor.execute("""
            SELECT 1 FROM characters 
            WHERE id = %s AND user_id = %s
        """, (data['character_id'], user_id))
        if not cursor.fetchone():
            return jsonify({'error': 'Personaje no válido o no te pertenece'}), 403
        
        # Verificar si ya está en la partida
        cursor.execute("""
            SELECT 1 FROM session_characters 
            WHERE session_id = %s AND character_id = %s
        """, (session_id, data['character_id']))
        if cursor.fetchone():
            return jsonify({'error': 'Ya estás en esta partida con este personaje'}), 400
        
        # Unir a la partida
        cursor.execute("""
            INSERT INTO session_characters 
            (session_id, character_id) 
            VALUES (%s, %s)
        """, (session_id, data['character_id']))
        
        conn.commit()
        return jsonify({'message': 'Unido a la partida exitosamente'}), 200
    except Error as e:
        conn.rollback()
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
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
        
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Verificar si es el Game Master
        cursor.execute("""
            SELECT 1 FROM game_sessions 
            WHERE id = %s AND game_master_id = %s
        """, (session_id, user_id))
        if not cursor.fetchone():
            return jsonify({'error': 'Solo el Game Master puede iniciar combate'}), 403
        
        # Verificar si ya hay un combate activo
        cursor.execute("""
            SELECT 1 FROM active_combats 
            WHERE session_id = %s AND status IN ('pending', 'active')
        """, (session_id,))
        if cursor.fetchone():
            return jsonify({'error': 'Ya hay un combate activo en esta sesión'}), 400
        
        # Crear encuentro de combate
        cursor.execute("""
            INSERT INTO active_combats 
            (session_id, encounter_id, status) 
            VALUES (%s, 1, 'pending')
        """, (session_id,))
        
        combat_id = cursor.lastrowid
        
        # Obtener personajes en la sesión
        cursor.execute("""
            SELECT sc.character_id, c.name, c.dexterity
            FROM session_characters sc
            JOIN characters c ON sc.character_id = c.id
            WHERE sc.session_id = %s AND sc.left_at IS NULL
        """, (session_id,))
        characters = cursor.fetchall()
        
        # Insertar participantes (personajes)
        for char in characters:
            initiative = roll_dice(20) + (char['dexterity'] - 10) // 2
            cursor.execute("""
                INSERT INTO combat_participants
                (combat_id, character_id, initiative, current_hp, max_hp, turn_order)
                VALUES (%s, %s, %s, 
                        (SELECT hit_points FROM characters WHERE id = %s),
                        (SELECT max_hit_points FROM characters WHERE id = %s),
                        %s)
            """, (combat_id, char['character_id'], initiative, 
                  char['character_id'], char['character_id'], 0))
        
        # Insertar enemigos (ejemplo con enemigos predefinidos)
        cursor.execute("SELECT id FROM enemies LIMIT 3")
        enemies = cursor.fetchall()
        
        for enemy in enemies:
            initiative = roll_dice(20) + 1  # Bonus de iniciativa simple para enemigos
            cursor.execute("""
                INSERT INTO combat_participants
                (combat_id, enemy_id, initiative, current_hp, max_hp, turn_order)
                VALUES (%s, %s, %s, 
                        (SELECT hit_points FROM enemies WHERE id = %s),
                        (SELECT hit_points FROM enemies WHERE id = %s),
                        %s)
            """, (combat_id, enemy['id'], initiative, 
                  enemy['id'], enemy['id'], 0))
        
        # Calcular orden de turno
        cursor.execute("""
            UPDATE combat_participants cp
            JOIN (
                SELECT id, ROW_NUMBER() OVER (ORDER BY initiative DESC) as turn_order
                FROM combat_participants
                WHERE combat_id = %s
            ) as ordered ON cp.id = ordered.id
            SET cp.turn_order = ordered.turn_order
            WHERE cp.combat_id = %s
        """, (combat_id, combat_id))
        
        # Actualizar estado del combate
        cursor.execute("""
            UPDATE active_combats 
            SET status = 'active', current_turn = 1
            WHERE id = %s
        """, (combat_id,))
        
        conn.commit()
        
        # Obtener información del combate para la respuesta
        cursor.execute("""
            SELECT ac.*, ce.description as encounter_description
            FROM active_combats ac
            LEFT JOIN combat_encounters ce ON ac.encounter_id = ce.id
            WHERE ac.id = %s
        """, (combat_id,))
        combat_info = cursor.fetchone()
        
        cursor.execute("""
            SELECT 
                cp.*,
                COALESCE(c.name, e.name) as name,
                CASE WHEN cp.character_id IS NOT NULL THEN 'character' ELSE 'enemy' END as type
            FROM combat_participants cp
            LEFT JOIN characters c ON cp.character_id = c.id
            LEFT JOIN enemies e ON cp.enemy_id = e.id
            WHERE cp.combat_id = %s
            ORDER BY cp.turn_order
        """, (combat_id,))
        participants = cursor.fetchall()
        
        return jsonify({
            'message': 'Combate iniciado exitosamente',
            'combat': {
                'id': combat_info['id'],
                'round': combat_info['round'],
                'current_turn': combat_info['current_turn'],
                'status': combat_info['status'],
                'description': combat_info['encounter_description'],
                'participants': participants
            }
        }), 200
    except Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()

def roll_dice(dice_type):
    import random
    return random.randint(1, dice_type)

# ---- Registro de Acciones ----
@app.route('/game_logs', methods=['POST'])
@jwt_required()
def log_action():
    data = request.json
    user_id = get_jwt_identity()
    
    required_fields = ['session_id', 'action_type', 'description']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Faltan campos requeridos: session_id, action_type, description'}), 400
    
    conn = get_db()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
        
    cursor = conn.cursor()
    
    try:
        # Verificar que el usuario está en la sesión
        cursor.execute("""
            SELECT 1 FROM session_characters sc
            JOIN characters c ON sc.character_id = c.id
            WHERE sc.session_id = %s AND c.user_id = %s AND sc.left_at IS NULL
        """, (data['session_id'], user_id))
        
        if not cursor.fetchone():
            return jsonify({'error': 'No estás en esta sesión o no tienes permisos'}), 403
        
        cursor.execute("""
            INSERT INTO game_logs 
            (session_id, character_id, action_type, description, details)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data['session_id'], 
            data.get('character_id'), 
            data['action_type'], 
            data['description'],
            json.dumps(data.get('details', {}))
        ))
        
        conn.commit()
        return jsonify({'message': 'Acción registrada exitosamente'}), 201
    except Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)