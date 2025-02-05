import requests

# Clase User
class User:
    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
    
    def __str__(self):
        return f"Id: {self.id}, Username: {self.username}, Password: {self.password}, Email: {self.email}"

# Clase Error
class Error:
    def __init__(self, codeError, description):
        self.codeError = codeError
        self.description = description

# Clase DaoUser
class DaoUser:
    def __init__(self):
        self.base_url = "http://localhost:10050/prototip1/getuser"  # URL del Backend

    def getUserByUsername(self, username):
        # Realiza la solicitud HTTP al Backend para obtener información del usuario
        response = requests.get(self.base_url, params={"username": username})
        
        if response.status_code == 200:
            user_data = response.json()
            return User(user_data['id'], user_data['username'], user_data['password'], user_data['email'])
        else:
            # Si el usuario no se encuentra, devuelve un error
            return Error(response.status_code, "User not found")

# Clase View (Console)
class View:
    def __init__(self):
        self.username = ""
        
    def getUsernameByConsole(self):
        # Obtiene el username ingresado por el usuario desde la consola
        return input("Enter username: ")
    
    def UserInfo(self, user):
        # Muestra la información del usuario
        if isinstance(user, User):
            print(f"User Info: {user}")
        else:
            print("User not found.")
    
    def ErrorInfo(self, error):
        # Muestra los detalles del error
        if isinstance(error, Error):
            print(f"Error {error.codeError}: {error.description}")

# Función principal
if __name__ == "__main__":
    # Crear las instancias de las clases
    view = View()
    dao_user = DaoUser()

    # Paso 1: Obtener el username desde la consola
    username = view.getUsernameByConsole()

    # Paso 2: Obtener la información del usuario a partir del username
    user = dao_user.getUserByUsername(username)

    # Paso 3: Mostrar la información del usuario o el error
    if isinstance(user, User):
        view.UserInfo(user)
    elif isinstance(user, Error):
        view.ErrorInfo(user)
