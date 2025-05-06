-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 30-04-2025 a las 12:40:12
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `rolplayer.bd`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `active_combats`
--

CREATE TABLE `active_combats` (
  `id` int(11) NOT NULL,
  `session_id` int(11) NOT NULL,
  `encounter_id` int(11) NOT NULL,
  `current_turn` int(11) NOT NULL DEFAULT 0,
  `round` int(11) NOT NULL DEFAULT 1,
  `status` enum('pending','active','completed','fled') NOT NULL DEFAULT 'pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `adventures`
--

CREATE TABLE `adventures` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `is_public` tinyint(1) NOT NULL DEFAULT 0,
  `difficulty` enum('Fácil','Normal','Difícil','Épico') NOT NULL DEFAULT 'Normal',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `characters`
--

CREATE TABLE `characters` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `race` enum('Humano','Elfo','Enano','Orco','Mediano') NOT NULL,
  `class` enum('Guerrero','Mago','Pícaro','Clérigo','Bárbaro','Bardo') NOT NULL,
  `level` int(11) NOT NULL DEFAULT 1,
  `experience` int(11) NOT NULL DEFAULT 0,
  `strength` int(11) NOT NULL DEFAULT 10,
  `dexterity` int(11) NOT NULL DEFAULT 10,
  `constitution` int(11) NOT NULL DEFAULT 10,
  `intelligence` int(11) NOT NULL DEFAULT 10,
  `wisdom` int(11) NOT NULL DEFAULT 10,
  `charisma` int(11) NOT NULL DEFAULT 10,
  `hit_points` int(11) NOT NULL DEFAULT 10,
  `max_hit_points` int(11) NOT NULL DEFAULT 10,
  `gold` int(11) NOT NULL DEFAULT 0,
  `background` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `character_items`
--

CREATE TABLE `character_items` (
  `id` int(11) NOT NULL,
  `character_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 1,
  `is_equipped` tinyint(1) NOT NULL DEFAULT 0
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `character_skills`
--

CREATE TABLE `character_skills` (
  `id` int(11) NOT NULL,
  `character_id` int(11) NOT NULL,
  `skill_id` int(11) NOT NULL,
  `proficiency_bonus` int(11) NOT NULL DEFAULT 2,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `character_spells`
--

CREATE TABLE `character_spells` (
  `id` int(11) NOT NULL,
  `character_id` int(11) NOT NULL,
  `spell_id` int(11) NOT NULL,
  `prepared` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `combat_encounters`
--

CREATE TABLE `combat_encounters` (
  `id` int(11) NOT NULL,
  `scene_id` int(11) NOT NULL,
  `description` text DEFAULT NULL,
  `difficulty` enum('Fácil','Moderado','Difícil','Mortal') NOT NULL DEFAULT 'Moderado',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `combat_participants`
--

CREATE TABLE `combat_participants` (
  `id` int(11) NOT NULL,
  `combat_id` int(11) NOT NULL,
  `character_id` int(11) DEFAULT NULL,
  `enemy_id` int(11) DEFAULT NULL,
  `initiative` int(11) NOT NULL,
  `current_hp` int(11) NOT NULL,
  `max_hp` int(11) NOT NULL,
  `conditions` text DEFAULT NULL,
  `turn_order` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `encounter_enemies`
--

CREATE TABLE `encounter_enemies` (
  `id` int(11) NOT NULL,
  `encounter_id` int(11) NOT NULL,
  `enemy_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 1,
  `current_hp` int(11) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `enemies`
--

CREATE TABLE `enemies` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `race` varchar(50) DEFAULT NULL,
  `level` int(11) NOT NULL DEFAULT 1,
  `strength` int(11) NOT NULL DEFAULT 10,
  `dexterity` int(11) NOT NULL DEFAULT 10,
  `constitution` int(11) NOT NULL DEFAULT 10,
  `intelligence` int(11) NOT NULL DEFAULT 10,
  `wisdom` int(11) NOT NULL DEFAULT 10,
  `charisma` int(11) NOT NULL DEFAULT 10,
  `hit_points` int(11) NOT NULL DEFAULT 10,
  `armor_class` int(11) NOT NULL DEFAULT 10,
  `attack_bonus` int(11) NOT NULL DEFAULT 2,
  `damage` varchar(20) NOT NULL DEFAULT '1d6',
  `xp_value` int(11) NOT NULL DEFAULT 50,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `game_logs`
--

CREATE TABLE `game_logs` (
  `id` int(11) NOT NULL,
  `session_id` int(11) NOT NULL,
  `character_id` int(11) DEFAULT NULL,
  `action_type` enum('move','combat','dialogue','item_use','skill_check','spell_cast','decision','system') NOT NULL,
  `description` text NOT NULL,
  `details` text DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `game_sessions`
--

CREATE TABLE `game_sessions` (
  `id` int(11) NOT NULL,
  `adventure_id` int(11) NOT NULL,
  `game_master_id` int(11) NOT NULL,
  `current_scene_id` int(11) DEFAULT NULL,
  `status` enum('pending','active','completed','abandoned') NOT NULL DEFAULT 'pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `items`
--

CREATE TABLE `items` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `type` enum('Arma','Armadura','Poción','Objeto mágico','Objeto común','Moneda') NOT NULL,
  `rarity` enum('Común','Poco común','Raro','Muy raro','Legendario') NOT NULL DEFAULT 'Común',
  `value` int(11) NOT NULL DEFAULT 0,
  `weight` decimal(10,2) NOT NULL DEFAULT 0.00,
  `attack_bonus` int(11) DEFAULT NULL,
  `damage` varchar(20) DEFAULT NULL,
  `armor_class` int(11) DEFAULT NULL,
  `healing_amount` int(11) DEFAULT NULL,
  `magic_effect` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `scenes`
--

CREATE TABLE `scenes` (
  `id` int(11) NOT NULL,
  `adventure_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `order` int(11) NOT NULL,
  `is_combat` tinyint(1) NOT NULL DEFAULT 0,
  `is_decision_point` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `scene_options`
--

CREATE TABLE `scene_options` (
  `id` int(11) NOT NULL,
  `scene_id` int(11) NOT NULL,
  `description` text NOT NULL,
  `next_scene_id` int(11) DEFAULT NULL,
  `success_message` text DEFAULT NULL,
  `failure_message` text DEFAULT NULL,
  `skill_check` varchar(50) DEFAULT NULL,
  `difficulty_class` int(11) DEFAULT NULL,
  `item_required` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `session_characters`
--

CREATE TABLE `session_characters` (
  `id` int(11) NOT NULL,
  `session_id` int(11) NOT NULL,
  `character_id` int(11) NOT NULL,
  `joined_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `left_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `skills`
--

CREATE TABLE `skills` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `ability` enum('strength','dexterity','constitution','intelligence','wisdom','charisma') NOT NULL,
  `is_proficient` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `spells`
--

CREATE TABLE `spells` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text NOT NULL,
  `level` int(11) NOT NULL DEFAULT 0,
  `school` enum('Abjuración','Conjuración','Adivinación','Encantamiento','Evocación','Ilusión','Nigromancia','Transmutación') NOT NULL,
  `casting_time` varchar(50) NOT NULL,
  `range` varchar(50) NOT NULL,
  `components` varchar(100) NOT NULL,
  `duration` varchar(100) NOT NULL,
  `damage` varchar(100) DEFAULT NULL,
  `healing` varchar(100) DEFAULT NULL,
  `effect` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `role` enum('admin','player','game_master') NOT NULL DEFAULT 'player',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `active_combats`
--
ALTER TABLE `active_combats`
  ADD PRIMARY KEY (`id`),
  ADD KEY `session_id` (`session_id`),
  ADD KEY `encounter_id` (`encounter_id`);

--
-- Indices de la tabla `adventures`
--
ALTER TABLE `adventures`
  ADD PRIMARY KEY (`id`),
  ADD KEY `created_by` (`created_by`);

--
-- Indices de la tabla `characters`
--
ALTER TABLE `characters`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indices de la tabla `character_items`
--
ALTER TABLE `character_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `character_id` (`character_id`),
  ADD KEY `item_id` (`item_id`);

--
-- Indices de la tabla `character_skills`
--
ALTER TABLE `character_skills`
  ADD PRIMARY KEY (`id`),
  ADD KEY `character_id` (`character_id`),
  ADD KEY `skill_id` (`skill_id`);

--
-- Indices de la tabla `character_spells`
--
ALTER TABLE `character_spells`
  ADD PRIMARY KEY (`id`),
  ADD KEY `character_id` (`character_id`),
  ADD KEY `spell_id` (`spell_id`);

--
-- Indices de la tabla `combat_encounters`
--
ALTER TABLE `combat_encounters`
  ADD PRIMARY KEY (`id`),
  ADD KEY `scene_id` (`scene_id`);

--
-- Indices de la tabla `combat_participants`
--
ALTER TABLE `combat_participants`
  ADD PRIMARY KEY (`id`),
  ADD KEY `combat_id` (`combat_id`),
  ADD KEY `character_id` (`character_id`),
  ADD KEY `enemy_id` (`enemy_id`);

--
-- Indices de la tabla `encounter_enemies`
--
ALTER TABLE `encounter_enemies`
  ADD PRIMARY KEY (`id`),
  ADD KEY `encounter_id` (`encounter_id`),
  ADD KEY `enemy_id` (`enemy_id`);

--
-- Indices de la tabla `enemies`
--
ALTER TABLE `enemies`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `game_logs`
--
ALTER TABLE `game_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `session_id` (`session_id`),
  ADD KEY `character_id` (`character_id`);

--
-- Indices de la tabla `game_sessions`
--
ALTER TABLE `game_sessions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `adventure_id` (`adventure_id`),
  ADD KEY `game_master_id` (`game_master_id`),
  ADD KEY `current_scene_id` (`current_scene_id`);

--
-- Indices de la tabla `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `scenes`
--
ALTER TABLE `scenes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `adventure_id` (`adventure_id`);

--
-- Indices de la tabla `scene_options`
--
ALTER TABLE `scene_options`
  ADD PRIMARY KEY (`id`),
  ADD KEY `scene_id` (`scene_id`),
  ADD KEY `next_scene_id` (`next_scene_id`),
  ADD KEY `item_required` (`item_required`);

--
-- Indices de la tabla `session_characters`
--
ALTER TABLE `session_characters`
  ADD PRIMARY KEY (`id`),
  ADD KEY `session_id` (`session_id`),
  ADD KEY `character_id` (`character_id`);

--
-- Indices de la tabla `skills`
--
ALTER TABLE `skills`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `spells`
--
ALTER TABLE `spells`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `active_combats`
--
ALTER TABLE `active_combats`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `adventures`
--
ALTER TABLE `adventures`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `characters`
--
ALTER TABLE `characters`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `character_items`
--
ALTER TABLE `character_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `character_skills`
--
ALTER TABLE `character_skills`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `character_spells`
--
ALTER TABLE `character_spells`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `combat_encounters`
--
ALTER TABLE `combat_encounters`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `combat_participants`
--
ALTER TABLE `combat_participants`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `encounter_enemies`
--
ALTER TABLE `encounter_enemies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `enemies`
--
ALTER TABLE `enemies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `game_logs`
--
ALTER TABLE `game_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `game_sessions`
--
ALTER TABLE `game_sessions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `items`
--
ALTER TABLE `items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `scenes`
--
ALTER TABLE `scenes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `scene_options`
--
ALTER TABLE `scene_options`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `session_characters`
--
ALTER TABLE `session_characters`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `skills`
--
ALTER TABLE `skills`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `spells`
--
ALTER TABLE `spells`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `active_combats`
--
ALTER TABLE `active_combats`
  ADD CONSTRAINT `active_combats_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `game_sessions` (`id`),
  ADD CONSTRAINT `active_combats_ibfk_2` FOREIGN KEY (`encounter_id`) REFERENCES `combat_encounters` (`id`);

--
-- Filtros para la tabla `adventures`
--
ALTER TABLE `adventures`
  ADD CONSTRAINT `adventures_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`);

--
-- Filtros para la tabla `characters`
--
ALTER TABLE `characters`
  ADD CONSTRAINT `characters_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Filtros para la tabla `character_items`
--
ALTER TABLE `character_items`
  ADD CONSTRAINT `character_items_ibfk_1` FOREIGN KEY (`character_id`) REFERENCES `characters` (`id`),
  ADD CONSTRAINT `character_items_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`);

--
-- Filtros para la tabla `character_skills`
--
ALTER TABLE `character_skills`
  ADD CONSTRAINT `character_skills_ibfk_1` FOREIGN KEY (`character_id`) REFERENCES `characters` (`id`),
  ADD CONSTRAINT `character_skills_ibfk_2` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`);

--
-- Filtros para la tabla `character_spells`
--
ALTER TABLE `character_spells`
  ADD CONSTRAINT `character_spells_ibfk_1` FOREIGN KEY (`character_id`) REFERENCES `characters` (`id`),
  ADD CONSTRAINT `character_spells_ibfk_2` FOREIGN KEY (`spell_id`) REFERENCES `spells` (`id`);

--
-- Filtros para la tabla `combat_encounters`
--
ALTER TABLE `combat_encounters`
  ADD CONSTRAINT `combat_encounters_ibfk_1` FOREIGN KEY (`scene_id`) REFERENCES `scenes` (`id`);

--
-- Filtros para la tabla `combat_participants`
--
ALTER TABLE `combat_participants`
  ADD CONSTRAINT `combat_participants_ibfk_1` FOREIGN KEY (`combat_id`) REFERENCES `active_combats` (`id`),
  ADD CONSTRAINT `combat_participants_ibfk_2` FOREIGN KEY (`character_id`) REFERENCES `characters` (`id`),
  ADD CONSTRAINT `combat_participants_ibfk_3` FOREIGN KEY (`enemy_id`) REFERENCES `enemies` (`id`);

--
-- Filtros para la tabla `encounter_enemies`
--
ALTER TABLE `encounter_enemies`
  ADD CONSTRAINT `encounter_enemies_ibfk_1` FOREIGN KEY (`encounter_id`) REFERENCES `combat_encounters` (`id`),
  ADD CONSTRAINT `encounter_enemies_ibfk_2` FOREIGN KEY (`enemy_id`) REFERENCES `enemies` (`id`);

--
-- Filtros para la tabla `game_logs`
--
ALTER TABLE `game_logs`
  ADD CONSTRAINT `game_logs_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `game_sessions` (`id`),
  ADD CONSTRAINT `game_logs_ibfk_2` FOREIGN KEY (`character_id`) REFERENCES `characters` (`id`);

--
-- Filtros para la tabla `game_sessions`
--
ALTER TABLE `game_sessions`
  ADD CONSTRAINT `game_sessions_ibfk_1` FOREIGN KEY (`adventure_id`) REFERENCES `adventures` (`id`),
  ADD CONSTRAINT `game_sessions_ibfk_2` FOREIGN KEY (`game_master_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `game_sessions_ibfk_3` FOREIGN KEY (`current_scene_id`) REFERENCES `scenes` (`id`);

--
-- Filtros para la tabla `scenes`
--
ALTER TABLE `scenes`
  ADD CONSTRAINT `scenes_ibfk_1` FOREIGN KEY (`adventure_id`) REFERENCES `adventures` (`id`);

--
-- Filtros para la tabla `scene_options`
--
ALTER TABLE `scene_options`
  ADD CONSTRAINT `scene_options_ibfk_1` FOREIGN KEY (`scene_id`) REFERENCES `scenes` (`id`),
  ADD CONSTRAINT `scene_options_ibfk_2` FOREIGN KEY (`next_scene_id`) REFERENCES `scenes` (`id`),
  ADD CONSTRAINT `scene_options_ibfk_3` FOREIGN KEY (`item_required`) REFERENCES `items` (`id`);

--
-- Filtros para la tabla `session_characters`
--
ALTER TABLE `session_characters`
  ADD CONSTRAINT `session_characters_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `game_sessions` (`id`),
  ADD CONSTRAINT `session_characters_ibfk_2` FOREIGN KEY (`character_id`) REFERENCES `characters` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
