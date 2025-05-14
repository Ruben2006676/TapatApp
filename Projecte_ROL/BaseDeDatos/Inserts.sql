-- USERS
INSERT INTO users (id, username, password, email, role) VALUES
(1, 'admin1', 'adminpass', 'admin@example.com', 'admin'),
(2, 'player1', 'playerpass', 'player1@example.com', 'player'),
(3, 'gm1', 'gmpass', 'gm@example.com', 'game_master');

-- ADVENTURES
INSERT INTO adventures (id, title, description, created_by, is_public, difficulty) VALUES
(1, 'La Torre Perdida', 'Una antigua torre llena de secretos.', 3, 1, 'Difícil'),
(2, 'El Bosque Maldito', 'Un bosque lleno de sombras y horrores.', 3, 1, 'Media'),
(3, 'Mazmorra del Eco', 'Ecos misteriosos resuenan en esta mazmorra abandonada.', 3, 0, 'Fácil');

-- SCENES
INSERT INTO scenes (id, adventure_id, title, description, `order`, is_combat, is_decision_point) VALUES
(1, 1, 'Entrada a la Torre', 'Los jugadores se enfrentan a la puerta mágica.', 1, 0, 1),
(2, 1, 'Vestíbulo', 'Una sala con esqueletos animados.', 2, 1, 0),
(3, 2, 'Sendero Oscuro', 'Un camino apenas visible entre los árboles.', 1, 0, 1);

-- SCENE_OPTIONS
INSERT INTO scene_options (id, scene_id, description, next_scene_id, success_message, failure_message) VALUES
(1, 1, 'Abrir la puerta con fuerza', 2, 'La puerta se abre con un crujido.', 'No logras abrirla.'),
(2, 1, 'Buscar un mecanismo oculto', 2, 'Encuentras una palanca secreta.', 'No hay ningún mecanismo.'),
(3, 3, 'Encender una antorcha', NULL, 'La luz revela el camino.', 'El viento apaga la antorcha.');

-- COMBAT_ENCOUNTERS
INSERT INTO combat_encounters (id, scene_id, description, difficulty) VALUES
(1, 2, 'Batalla contra esqueletos guardianes.', 'Moderado'),
(2, 3, 'Lobos salvajes emergen del bosque.', 'Fácil'),
(3, 2, 'Una trampa mágica se activa.', 'Difícil');

-- ENEMIES
INSERT INTO enemies (id, name, description, race, level, strength, dexterity, constitution, intelligence, wisdom, charisma, hit_points, armor_class, attack_bonus, damage, xp_value) VALUES
(1, 'Esqueleto Guerrero', 'Un esqueleto armado con espada oxidada.', 'No muerto', 2, 12, 10, 11, 5, 8, 5, 13, 13, 3, '1d8', 100),
(2, 'Lobo Salvaje', 'Una bestia feroz y hambrienta.', 'Bestia', 1, 13, 15, 12, 2, 12, 6, 11, 12, 2, '1d6+1', 50),
(3, 'Mago Espectral', 'Un espíritu oscuro con poderes mágicos.', 'No muerto', 3, 8, 12, 10, 15, 14, 10, 20, 12, 4, '2d6', 200);

-- ENCOUNTER_ENEMIES
INSERT INTO encounter_enemies (id, encounter_id, enemy_id, quantity) VALUES
(1, 1, 1, 3),
(2, 2, 2, 2),
(3, 3, 3, 1);

-- GAME_SESSIONS
INSERT INTO game_sessions (id, adventure_id, game_master_id, current_scene_id, status) VALUES
(1, 1, 3, 1, 'active'),
(2, 2, 3, 3, 'waiting'),
(3, 3, 3, NULL, 'completed');

-- ACTIVE_COMBATS
INSERT INTO active_combats (id, session_id, encounter_id, current_turn, round, status) VALUES
(1, 1, 1, 1, 1, 'active'),
(2, 2, 2, 2, 3, 'paused'),
(3, 3, 3, 1, 1, 'ended');

-- SKILLS
INSERT INTO skills (id, name, description, ability) VALUES
(1, 'Acrobacias', 'Permite maniobras ágiles.', 'dexterity'),
(2, 'Historia', 'Conocimiento de eventos pasados.', 'intelligence'),
(3, 'Persuasión', 'Influye en otras personas.', 'charisma');

-- SPELLS
INSERT INTO spells (id, name, description, level, school, casting_time, range, components, duration) VALUES
(1, 'Misil Mágico', 'Lanza dardos de energía mágica.', 1, 'Evocación', '1 acción', '120 pies', 'V,S', 'Instantáneo'),
(2, 'Curar Heridas', 'Restaura puntos de golpe.', 1, 'Conjuración', '1 acción', 'Toque', 'V,S', 'Instantáneo'),
(3, 'Escudo', 'Aumenta la clase de armadura temporalmente.', 1, 'Abjuración', '1 reacción', 'Personal', 'V,S', '1 turno');

-- ITEMS
INSERT INTO items (id, name, description, type, rarity, value, weight, attack_bonus, damage, armor_class, healing_amount) VALUES
(1, 'Espada Corta', 'Arma básica de filo.', 'Arma', 'Común', 10, 2.0, 1, '1d6', NULL, NULL),
(2, 'Poción de Curación', 'Recupera salud.', 'Poción', 'Común', 50, 0.5, NULL, NULL, NULL, 10),
(3, 'Escudo de Roble', 'Escudo resistente de madera.', 'Armadura', 'Incomún', 75, 6.0, NULL, NULL, 2, NULL);

-- CHARACTERS
INSERT INTO characters (id, user_id, name, race, class, level, experience, strength, dexterity, constitution, intelligence, wisdom, charisma, hit_points, max_hit_points, gold, background) VALUES
(1, 2, 'Arthas', 'Humano', 'Guerrero', 2, 150, 14, 12, 13, 10, 10, 10, 18, 18, 50, 'Soldado caído en desgracia.'),
(2, 2, 'Elandra', 'Elfo', 'Maga', 3, 320, 8, 14, 11, 16, 12, 13, 12, 12, 75, 'Estudiosa de lo arcano.'),
(3, 2, 'Thorin', 'Enano', 'Clérigo', 2, 200, 13, 10, 14, 10, 15, 9, 16, 16, 40, 'Exiliado de su clan.');

-- CHARACTER_SKILLS
INSERT INTO character_skills (id, character_id, skill_id, proficiency_bonus) VALUES
(1, 1, 1, 2),
(2, 2, 2, 2),
(3, 3, 3, 2);

-- CHARACTER_SPELLS
INSERT INTO character_spells (id, character_id, spell_id, prepared) VALUES
(1, 2, 1, 1),
(2, 2, 3, 1),
(3, 3, 2, 1);

-- CHARACTER_ITEMS
INSERT INTO character_items (id, character_id, item_id, quantity, is_equipped) VALUES
(1, 1, 1, 1, 1),
(2, 2, 2, 2, 0),
(3, 3, 3, 1, 1);

-- SESSION_CHARACTERS
INSERT INTO session_characters (id, session_id, character_id) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 2, 3);

-- COMBAT_PARTICIPANTS
INSERT INTO combat_participants (id, combat_id, character_id, enemy_id, initiative, current_hp, max_hp, turn_order) VALUES
(1, 1, 1, NULL, 15, 18, 18, 1),
(2, 1, NULL, 1, 12, 13, 13, 2),
(3, 1, 2, NULL, 18, 12, 12, 0);

-- GAME_LOGS
INSERT INTO game_logs (id, session_id, character_id, action_type, description) VALUES
(1, 1, 1, 'combat', 'Arthas ataca al esqueleto y lo golpea.'),
(2, 1, NULL, 'system', 'El combate ha comenzado.'),
(3, 2, 3, 'roleplay', 'Thorin ora por protección divina.');
