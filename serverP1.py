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
    
    def to_a_string(self):  # Pasamos a string/diccionario los datos para que jsonify funcione.
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password
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
        # Buscamos el usuario por el nombre de usuario
        for u in self.users:
            if u.username == username:
                return u
        return None

# Instancia del DAOUsers
daoUser = DAOUsers()

# Creación de la aplicación Flask
app = Flask(__name__)

# Ruta para obtener el usuario por parámetros en la URL
@app.route('/tapatapp/getuser', methods=['GET'])
def getUser():
    # Obtenemos los parámetros 'name' y 'email' de la consulta
    name = request.args.get('name')
    email = request.args.get('email')

    # Validación de los parámetros
    if not name or not email:
        return jsonify({"error": "Parametro no introducido"}), 400  # Respuesta si falta algún parámetro
    
    # Buscamos al usuario por nombre de usuario
    user = daoUser.getUserByUsername(name)

    if user and user.email == email:
        # Si encontramos al usuario y el email coincide
        return jsonify({
            "message": f"Usuari trobat: Nom={user.username}, email={user.email}, ID={user.id}, password={user.password}"
        }), 200
    else:
        # Si no se encuentra al usuario o el email no coincide
        return jsonify({"error": "Usuari no trobat"}), 404

# Arrancamos el servidor en el puerto 10050, según tu configuración de host.
if __name__ == '__main__':
    app.run(host='192.168.144.140', port=10050, debug=True)
