# Descripció del projecte RolPlayer

## 1. Introducción
RolPlayer es una aplicación de escritorio diseñada para gestionar partidas de rol (RPG), permitiendo a jugadores y directores de juego (Game Masters) crear personajes, organizar sesiones, simular combates y registrar acciones.

### Componentes principales:
- **Backend API**: Flask + MySQL.
- **Frontend**: Tkinter.
- **Base de Datos**: MySQL.

---

## 2. Funcionalidades Principales

### 2.1. Autenticación y Gestión de Usuarios
- **Registro/Login**: Los usuarios pueden iniciar sesión con username y contraseña (JWT).
- **Roles**:
  - **Player**: Puede crear y gestionar personajes.
  - **Game Master**: Además de lo anterior, puede crear partidas y controlar combates.
  - **Admin**: Acceso total.

### 2.2. Gestión de Personajes
- **Creación de personajes**:
  - Razas: Humano, Elfo, Enano, Orco, Mediano.
  - Clases: Guerrero, Mago, Pícaro, Clérigo, Bárbaro, Bardo.
  - Atributos: Fuerza, Destreza, Constitución, Inteligencia, Sabiduría, Carisma.
  - Salud, nivel, experiencia, oro y trasfondo.
- **Inventario**:
  - Objetos: armas, armaduras, pociones.
  - Cantidad y estado (equipado/no equipado).
- **Habilidades y Hechizos**:
  - Asignación de habilidades con bonificaciones.
  - Lista de hechizos preparados.

### 2.3. Partidas y Sesiones
- **Creación de partidas**:
  - Vinculadas a una aventura (escenarios predefinidos).
  - Estado: pendiente, activa, completada, abandonada.
- **Unión a partidas**:
  - Los jugadores pueden unirse con sus personajes.
  - El Game Master controla el progreso.

### 2.4. Sistema de Combate
- **Iniciativa**: Orden de turnos basado en tiradas de dados.
- **Participantes**:
  - Personajes jugadores (PCs).
  - Enemigos (NPCs con estadísticas predefinidas).
- **Mecánicas por turnos**:
  - Ataques, daño, curación.
  - Registro de condiciones (veneno, aturdimiento, etc.).

### 2.5. Registro de Acciones (Game Logs)
- **Historial de eventos en la partida**:
  - Movimientos.
  - Combates.
  - Diálogos.
  - Uso de objetos.
  - Tiradas de habilidad.

---

## 3. Arquitectura Técnica

### 3.1. Backend (Flask + JWT)
El backend está desarrollado en Flask y utiliza JWT para la autenticación. A continuación, se describen los endpoints principales:

#### Endpoints principales:

##### **Autenticación**
- **POST /login**
  - **Descripción**: Permite a los usuarios iniciar sesión con su nombre de usuario y contraseña.
  - **Parámetros**:
    - `username` (string): Nombre de usuario.
    - `password` (string): Contraseña.
  - **Respuesta**:
    - `access_token` (string): Token JWT para autenticación.
    - `refresh_token` (string): Token para renovar el acceso.
    - `user` (objeto): Información del usuario (id, username, role, personajes asociados).

##### **Gestión de Personajes**
- **POST /characters**
  - **Descripción**: Crea un nuevo personaje asociado al usuario autenticado.
  - **Parámetros**:
    - `name` (string): Nombre del personaje.
    - `race` (string): Raza del personaje (Humano, Elfo, etc.).
    - `class` (string): Clase del personaje (Guerrero, Mago, etc.).
    - `background` (string, opcional): Historia del personaje.
  - **Respuesta**:
    - `character` (objeto): Detalles del personaje creado.

- **GET /characters**
  - **Descripción**: Obtiene la lista de personajes del usuario autenticado.
  - **Respuesta**:
    - `characters` (array): Lista de personajes con detalles básicos.

- **GET /characters/<int:character_id>**
  - **Descripción**: Obtiene los detalles completos de un personaje específico.
  - **Respuesta**:
    - `character` (objeto): Detalles del personaje, incluyendo inventario, habilidades y hechizos.

##### **Gestión de Partidas**
- **POST /game_sessions**
  - **Descripción**: Crea una nueva partida asociada al usuario autenticado como Game Master.
  - **Parámetros**:
    - `adventure_id` (int): ID de la aventura asociada.
  - **Respuesta**:
    - `session_id` (int): ID de la partida creada.

- **POST /game_sessions/<int:session_id>/join**
  - **Descripción**: Permite a un usuario unirse a una partida con un personaje.
  - **Parámetros**:
    - `character_id` (int): ID del personaje que se unirá a la partida.
  - **Respuesta**:
    - `message` (string): Confirmación de la unión.

##### **Sistema de Combate**
- **POST /combat/<int:session_id>/start**
  - **Descripción**: Inicia un combate en una partida específica.
  - **Parámetros**:
    - `session_id` (int): ID de la partida.
  - **Respuesta**:
    - `combat` (objeto): Detalles del combate, incluyendo participantes y orden de turnos.

##### **Registro de Acciones**
- **POST /game_logs**
  - **Descripción**: Registra una acción realizada en una partida.
  - **Parámetros**:
    - `session_id` (int): ID de la partida.
    - `action_type` (string): Tipo de acción (movimiento, combate, diálogo, etc.).
    - `description` (string): Descripción de la acción.
    - `details` (objeto, opcional): Detalles adicionales de la acción.
  - **Respuesta**:
    - `message` (string): Confirmación del registro.


### 3.2. Frontend (Tkinter)
El frontend está desarrollado en Tkinter y utiliza una arquitectura basada en DAO (Data Access Object) para interactuar con el backend. A continuación, se describen las interfaces clave:

#### Interfaces clave:
- **Login**: Permite a los usuarios autenticarse con su nombre de usuario y contraseña.
- **Personajes**:
  - Listado de personajes del usuario.
  - Creación de nuevos personajes.
  - Visualización de detalles de personajes, incluyendo estadísticas, inventario, habilidades y hechizos.
- **Partidas**:
  - Creación de nuevas partidas (Game Master).
  - Unión a partidas existentes con un personaje.
- **Combate**:
  - Simulación de combates por turnos (solo para Game Masters).


## 4. Requerimientos Técnicos

### Backend
- **Lenguaje**: Python 3.9+
- **Framework**: Flask
- **Autenticación**: Flask-JWT-Extended para manejo de tokens JWT.
- **Base de Datos**: MySQL 8.0+
  - Tablas principales: users, characters, game_sessions, combat_participants, items, skills, spells.
- **Conexión a la Base de Datos**: MySQL Connector.
- **Librerías adicionales**:
  - `flask`: Para la creación de la API REST.
  - `flask-jwt-extended`: Para la autenticación basada en JWT.
  - `mysql-connector-python`: Para la conexión con la base de datos MySQL.

### Frontend
- **Lenguaje**: Python 3.9+
- **Framework**: Tkinter
- **Librerías adicionales**:
  - `Pillow`: Para manejo de imágenes (logos, íconos, etc.).
  - `requests`: Para realizar peticiones HTTP al backend.
- **Estilo**:
  - Tema oscuro con colores personalizados.
  - Diseño responsive adaptado a diferentes tamaños de ventana.
- **Arquitectura**:
  - Uso de clases DAO (Data Access Object) para separar la lógica de negocio de la interfaz gráfica.
  - Almacenamiento local en memoria para tokens y datos del usuario.



