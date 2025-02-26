import requests

# Clase User
class User:
    def __init__(self, id, username, email, password, first_name, last_name):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return (f"Id: {self.id}, Username: {self.username}, Email: {self.email}, "
                f"Nombre: {self.first_name} {self.last_name}")

# Clase Child
class Child:
    def __init__(self, id, user_id, name, birth_date, medical_info):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.birth_date = birth_date
        self.medical_info = medical_info

    def __str__(self):
        return (f"Id: {self.id}, Nombre: {self.name}, "
                f"Fecha de Nacimiento: {self.birth_date}, "
                f"Información Médica: {self.medical_info}")

# Clase Tap
class Tap:
    def __init__(self, id, child_id, date, time, status, total_hours):
        self.id = id
        self.child_id = child_id
        self.date = date
        self.time = time
        self.status = status
        self.total_hours = total_hours

    def __str__(self):
        return (f"Id: {self.id}, Fecha: {self.date}, Hora: {self.time}, "
                f"Estado: {self.status}, Horas Totales: {self.total_hours}")

# Clase Error
class Error:
    def __init__(self, code_error, description):
        self.code_error = code_error
        self.description = description

    def __str__(self):
        return f"Error {self.code_error}: {self.description}"

# Clase DaoUser
class DaoUser:
    def __init__(self):
        self.base_url = "http://127.0.0.1:5000"

    def get_user_by_credentials(self, user_id, password):
        try:
            response = requests.post(
                f"{self.base_url}/login",
                json={"id": user_id, "password": password}
            )

            if response.status_code == 200:
                user_data = response.json().get("user")
                return User(
                    user_data.get("id"),
                    user_data.get("username"),
                    user_data.get("email"),
                    password,
                    user_data.get("first_name"),
                    user_data.get("last_name")
                )
            else:
                return Error(response.status_code, response.json().get("error", "Error desconocido"))
        except requests.exceptions.ConnectionError:
            return Error(500, "Error de conexión: No se pudo conectar con el servidor")
        except requests.exceptions.RequestException as e:
            return Error(500, f"Error inesperado: {str(e)}")

# Clase DaoChild
class DaoChild:
    def __init__(self):
        self.base_url = "http://127.0.0.1:5000"

    def get_children_by_user(self, user_id):
        try:
            response = requests.get(
                f"{self.base_url}/child",
                params={"user_id": user_id}
            )

            if response.status_code == 200:
                children_data = response.json()
                return [Child(
                    child.get("id"),
                    child.get("user_id"),
                    child.get("name"),
                    child.get("birth_date"),
                    child.get("medical_info")
                ) for child in children_data]
            else:
                return Error(response.status_code, response.json().get("error", "Error desconocido"))
        except requests.exceptions.ConnectionError:
            return Error(500, "Error de conexión: No se pudo conectar con el servidor")
        except requests.exceptions.RequestException as e:
            return Error(500, f"Error inesperado: {str(e)}")

# Clase DaoTap
class DaoTap:
    def __init__(self):
        self.base_url = "http://127.0.0.1:5000"

    def get_tap_history_by_user(self, user_id):
        try:
            response = requests.get(
                f"{self.base_url}/tap/history",
                params={"user_id": user_id}
            )

            if response.status_code == 200:
                tap_history_data = response.json()
                return [Tap(
                    tap.get("id"),
                    tap.get("child_id"),
                    tap.get("date"),
                    tap.get("time"),
                    tap.get("status"),
                    tap.get("total_hours")
                ) for tap in tap_history_data]
            else:
                return Error(response.status_code, response.json().get("error", "Error desconocido"))
        except requests.exceptions.ConnectionError:
            return Error(500, "Error de conexión: No se pudo conectar con el servidor")
        except requests.exceptions.RequestException as e:
            return Error(500, f"Error inesperado: {str(e)}")

# Clase View (Consola)
class View:
    def get_credentials_by_console(self):
        user_id = int(input("Ingrese el ID de usuario: ").strip())
        password = input("Ingrese la contraseña: ").strip()
        return user_id, password

    def show_user_info(self, user):
        if isinstance(user, User):
            print(f"\nInformación del Usuario:\n{user}")
        else:
            print("\nNo se pudo obtener la información del usuario.")

    def show_children_info(self, children):
        if isinstance(children, list):
            print("\nInformación de los Niños:")
            for child in children:
                print(child)
        else:
            print("\nNo se pudo obtener la información de los niños.")

    def show_tap_history(self, tap_history):
        if isinstance(tap_history, list):
            print("\nHistorial de Taps:")
            for tap in tap_history:
                print(tap)
        else:
            print("\nNo se pudo obtener el historial de taps.")

    def show_error(self, error):
        if isinstance(error, Error):
            print(f"\n{error}")

# Función principal
if __name__ == "__main__":
    view = View()
    dao_user = DaoUser()
    dao_child = DaoChild()
    dao_tap = DaoTap()

    # Obtener credenciales del usuario
    user_id, password = view.get_credentials_by_console()

    # Obtener usuario del backend
    user = dao_user.get_user_by_credentials(user_id, password)

    # Mostrar información del usuario
    view.show_user_info(user)

    if isinstance(user, User):
        # Obtener información de los niños
        children = dao_child.get_children_by_user(user.id)
        view.show_children_info(children)

        # Obtener historial de taps
        tap_history = dao_tap.get_tap_history_by_user(user.id)
        view.show_tap_history(tap_history)