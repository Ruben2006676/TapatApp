from flask import Flask, request, jsonify
import webbrowser  # Para abrir la URL en el navegador

# Clase User
class User:
    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
    
    def __str__(self):
        return f"User: {self.username} pass: {self.password} email: {self.email}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

# Lista de usuarios
ListUsers = [
    User(id=1, username="usuari1", password="12345", email="prova@gmail.com"),
    User(id=2, username="usuari2", password="123", email="usuari2@gmail.com"),
    User(id=3, username="admin", password="12", email="admin@proven.cat")
]

# Clase DAOUsers
class DAOUsers:
    def __init__(self):
        self.users = ListUsers
    
    def getUserByUsername(self, username):
        for u in self.users:
            if u.username == username:
                return u
        return None

daoUser = DAOUsers()

# Configuración de la app Flask
app = Flask(__name__)

@app.route('/prototip/getuser/<string:username>', methods=['GET'])
def prototipGetUser(username):
    user = daoUser.getUserByUsername(username)
    
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({"error": "Usuari no trobat"}), 404

if __name__ == '__main__':
    # Dirección y puerto de la aplicación Flask
    host = "0.0.0.0"
    port = 10050

    # URL que devuelve JSON para un usuario específico
    username = "usuari1"  # Puedes cambiar este usuario según lo que quieras probar
    url = f"http://127.0.0.1:{port}/prototip/getuser/{username}"

    # Abrir el navegador automáticamente
    webbrowser.open(url)

    # Ejecutar la aplicación Flask
    app.run(debug=True, host=host, port=port)
