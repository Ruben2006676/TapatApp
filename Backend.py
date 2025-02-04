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

    def to_dict(self):  # Devuelve solo los datos necesarios
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

# Clase DAOUsers para gestionar la obtención de usuarios
class DAOUsers:
    def __init__(self):
        self.users = ListUsers

    def get_user_data(self, username):
        """Busca un usuario por username y devuelve solo id, username y email."""
        for user in self.users:
            if user.username == username:
                return user.to_dict()  # Devolvemos solo los datos necesarios
        return None  # Si no se encuentra, devolvemos None

# Instancia del DAOUsers
daoUser = DAOUsers()

# Creación de la aplicación Flask
app = Flask(__name__)

# Ruta para obtener el usuario por parámetros en la URL
@app.route('/tapatapp/getuser', methods=['GET'])
def getUser():
    try:
        # Obtenemos los parámetros 'username' y 'email' de la consulta
        username = request.args.get('username')
        email = request.args.get('email')

        # Validación de los parámetros
        if not username or not email:
            return jsonify({"error": "Paràmetre no introduit"}), 400  # Respuesta si falta algún parámetro

        # Buscamos los datos del usuario
        user_data = daoUser.get_user_data(username)

        if user_data and user_data["email"] == email:
            # Si encontramos al usuario y el email coincide
            return jsonify({
                "message": f"Usuari trobat: Nom={user_data['username']}, email={user_data['email']}, ID={user_data['id']}"
            }), 200
        else:
            # Si no se encuentra al usuario o el email no coincide
            return jsonify({"error": "Usuari no trobat"}), 404

    except Exception as e:
        # Errores internos del servidor
        return jsonify({"description": "Server Error"}), 500

# Arrancamos el servidor en el puerto 10050, según tu configuración de host.
if __name__ == '__main__':
    app.run(host='192.168.144.140', port=10050, debug=True)

