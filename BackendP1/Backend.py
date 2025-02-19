from flask import Flask, request, jsonify

# Clase User
class User:
    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
    
    def __str__(self):
        return f"User: {self.username} email: {self.email}"
    
    def to_dict(self):  # Convertir el usuario a diccionario
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password  # Ahora también incluye la contraseña
        }

# Lista de usuarios
ListUsers = [
    User(id=1, username="usuari1", password="12345", email="prova@gmail.com"),
    User(id=2, username="usuari2", password="123", email="usuari2@gmail.com"),
    User(id=3, username="admin", password="12", email="admin@proven.cat")
]

# Imprimir usuarios en consola al iniciar
for u in ListUsers:
    print(u)

# Clase DAOUsers
class DAOUsers:
    def __init__(self):
        self.users = ListUsers
    
    def getUserByUsername(self, username):
        return next((u for u in self.users if u.username == username), None)

# Instancia del DAOUsers
daoUser = DAOUsers()

# Creación de la aplicación Flask
app = Flask(__name__)

# Ruta para obtener usuario por credenciales
@app.route('/tapatapp/getuser', methods=['GET'])
def getUser():
    try:
        username = request.args.get('username', '').strip()
        email = request.args.get('email', '').strip()
        password = request.args.get('password', '').strip()

        # Validar que todos los parámetros estén presentes
        if not username or not email or not password:
            return jsonify({"error": "Faltan datos: username, email y password son requeridos"}), 400
        
        user = daoUser.getUserByUsername(username)

        if user is None:
            return jsonify({"error": "Usuario no encontrado"}), 404

        if user.email != email:
            return jsonify({"error": "Email incorrecto"}), 401

        if user.password != password:
            return jsonify({"error": "Contraseña incorrecta"}), 401

        return jsonify(user.to_dict()), 200

    except Exception as e:
        print(f"Error inesperado: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

# Iniciar el servidor en la IP correcta
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=10050, debug=True)

