import requests

# Clase User
class User:
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password  # Ahora también mostramos la contraseña

    def __str__(self):
        return f"Id: {self.id}, Username: {self.username}, Email: {self.email}, Password: {self.password}"

# Clase Error
class Error:
    def __init__(self, codeError, description):
        self.codeError = codeError
        self.description = description

# Clase DaoUser
class DaoUser:
    def __init__(self):
        # URL del Backend
        self.base_url = "http://127.0.0.1:10050/tapatapp/getuser"

    def getUserByCredentials(self, username, email, password):
        try:
            # Validar que los campos no estén vacíos
            if not username or not email or not password:
                return Error(400, "Todos los campos son obligatorios")

            params = {"username": username, "email": email, "password": password}
            response = requests.get(self.base_url, params=params)

            if response.status_code == 200:
                user_data = response.json()
                return User(user_data.get('id'), user_data.get('username'), user_data.get('email'), password)
            elif response.status_code in [400, 401, 404]:
                return Error(response.status_code, response.json().get("error", "Error desconocido"))
            else:
                return Error(response.status_code, "Error desconocido en el servidor")
        except requests.exceptions.ConnectionError:
            return Error(500, "Error de conexión: No se pudo conectar con el servidor")
        except requests.exceptions.RequestException as e:
            return Error(500, f"Error inesperado: {str(e)}")

# Clase View (Consola)
class View:
    def getCredentialsByConsole(self):
        username = input("Ingrese el nombre de usuario: ").strip()
        email = input("Ingrese el email: ").strip()
        password = input("Ingrese la contraseña: ").strip()
        return username, email, password
    
    def UserInfo(self, user):
        if isinstance(user, User):
            print(f"\nUsuario encontrado:\n{user}")
        else:
            print("\nUsuario no encontrado.")

    def ErrorInfo(self, error):
        if isinstance(error, Error):
            print(f"\nError {error.codeError}: {error.description}")

# Función principal
if __name__ == "__main__":
    view = View()
    dao_user = DaoUser()

    # Obtener credenciales del usuario
    username, email, password = view.getCredentialsByConsole()

    # Obtener usuario del backend
    user = dao_user.getUserByCredentials(username, email, password)

    # Mostrar resultado
    if isinstance(user, User):
        view.UserInfo(user)
    elif isinstance(user, Error):
        view.ErrorInfo(user)
