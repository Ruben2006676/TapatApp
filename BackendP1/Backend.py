from flask import Flask, request, jsonify

# Clase User
class User:
    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
    
    def __str__(self):
        return f"User: {self.username} pass: {self.password} email: {self.email}"
    
    def to_dict(self):  # Pasamos a diccionario los datos para que jsonify funcione correctamente.
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

# Lista de usuarios iniciales
ListUsers = [
    User(id=1, username="usuari1", password="12345", email="prova@gmail.com"),
    User(id=2, username="usuari2", password="123", email="usuari2@gmail.com"),
    User(id=3, username="admin", password="12", email="admin@proven.cat")
]

# Se imprimen los usuarios al inicio para verificar
for u in ListUsers:
    print(u)

# Clase DAOUsers para gestionar la obtención de usuarios
class DAOUsers:
    def __init__(self):
        self.users = ListUsers
    
    def getUserByUsername(self, username):
        return next((u for u in self.users if u.username == username), None)

# Instancia del DAOUsers
daoUser = DAOUsers()

# Creación de la aplicación Flask
app = Flask(__name__)

# Ruta para obtener el usuario por parámetros en la URL
@app.route('/tapatapp/getuser', methods=['GET'])
def getUser():
    try:
        name = request.args.get('name', '').strip()
        email = request.args.get('email', '').strip()
        password = request.args.get('password', '').strip()

        if not name or not email or not password:
            return jsonify({"error": "Falta algún parámetro"}), 400
        
        user = daoUser.getUserByUsername(name)

        if user is None:
            return jsonify({"error": "Usuario no encontrado"}), 404

        if user.email != email:
            return jsonify({"error": "Email incorrecto"}), 401

        if user.password != password:
            return jsonify({"error": "Contraseña incorrecta"}), 401

        return jsonify({
            "message": "Usuario encontrado",
            "user": user.to_dict()
        }), 200

    except Exception as e:
        print(f"Error inesperado: {e}")
        return jsonify({"description": "Error interno del servidor"}), 500

# Arrancamos el servidor en el puerto 10050, según tu configuración de host.
if __name__ == '__main__':
    app.run(host='192.168.144.140', port=10050, debug=True)

