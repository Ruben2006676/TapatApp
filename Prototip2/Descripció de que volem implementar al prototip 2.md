# Descripción del Prototipo 2

## Objetivo General

El Prototipo 2 tiene como objetivo desarrollar un sistema integral para gestionar la información de usuarios, niños y sus respectivos registros de actividad (taps). Este sistema permitirá a los usuarios (padres, tutores o cuidadores) acceder a la información de los niños bajo su responsabilidad, así como consultar el historial de actividades relacionadas con el uso de parches oculares (taps) y su estado (dormido, despierto, etc.).

## Funcionalidades Principales

### Autenticación de Usuarios:

Los usuarios podrán iniciar sesión en el sistema utilizando su ID y contraseña.

El sistema validará las credenciales y devolverá la información del usuario si la autenticación es exitosa.

### Gestión de Usuarios:

Los usuarios tendrán un perfil con información personal (nombre, apellido, nombre de usuario, correo electrónico y contraseña).

Los usuarios podrán ser padres, tutores o cuidadores.

### Gestión de Niños:

Cada usuario podrá tener uno o más niños asociados.

La información de cada niño incluirá:

Nombre.

Fecha de nacimiento.

Información médica relevante (por ejemplo, alergias o condiciones especiales).

### Registro de Taps:

Los taps representan actividades o eventos relacionados con el uso de parches oculares.

Cada tap incluirá:

Fecha y hora de inicio y fin.

Estado (dormido, despierto, con parche, sin parche).

Horas totales de uso.

## Consultas y Visualización:

Los usuarios podrán consultar:

La información de los niños asociados a su cuenta.

El historial de taps de cada niño.

La información se mostrará de manera clara y organizada en la interfaz de usuario.

## Componentes del Sistema

## Frontend (Cliente):

### Interfaz de Usuario (View):

Permite a los usuarios interactuar con el sistema (iniciar sesión, consultar información, etc.).

Muestra la información de usuarios, niños y taps de manera clara y accesible.

### Servicio Web (WebService):

Se comunica con el backend para enviar y recibir datos.

Gestiona las solicitudes del usuario (login, consultas, etc.).

### DAO (Objetos de Acceso a Datos):

DAOUsuarios: Gestiona la información de los usuarios.

DAONiños: Gestiona la información de los niños.

DAOTaps: Gestiona el historial de taps.

## Backend (Servidor):

### Servicio Web (WebService):

Recibe las solicitudes del frontend y las procesa.

Se comunica con las clases DAO para acceder a los datos.

DAO (Objetos de Acceso a Datos):

DAOUsuarios: Accede y gestiona la información de los usuarios.

DAONiños: Accede y gestiona la información de los niños.

DAOTaps: Accede y gestiona el historial de taps.

### Modelos de Datos:

Usuario: Representa a un usuario del sistema.

Niño: Representa a un niño asociado a un usuario.

Tap: Representa un registro de actividad (uso de parche ocular).

### Inicio de Sesión:

El usuario ingresa su ID y contraseña en la interfaz.

El frontend envía las credenciales al backend.

El backend valida las credenciales y devuelve la información del usuario si son correctas.

### Consulta de Niños:

El usuario solicita la información de los niños asociados a su cuenta.

El frontend envía la solicitud al backend.

El backend consulta la base de datos y devuelve la lista de niños.

### Consulta de Historial de Taps:

El usuario selecciona un niño y solicita su historial de taps.

El frontend envía la solicitud al backend.

El backend consulta la base de datos y devuelve el historial de taps del niño.

### Registro de Taps:

El usuario registra un nuevo tap (actividad) para un niño.

El frontend envía los datos del tap al backend.

El backend almacena el tap en la base de datos.
