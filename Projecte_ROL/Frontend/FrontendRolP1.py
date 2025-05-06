
import tkinter as tk
from tkinter import ttk, messagebox
import json
import requests
from datetime import datetime

# Configuración de estilos
def configure_styles():
    style = ttk.Style()
    style.configure('TFrame', background='#f0f0f0')
    style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
    style.configure('TButton', font=('Arial', 10), padding=5)
    style.configure('TEntry', font=('Arial', 10))
    style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
    style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
    style.configure('TNotebook', background='#f0f0f0')
    style.configure('TNotebook.Tab', padding=[10, 5])
    style.map('TButton', 
              foreground=[('active', 'black'), ('!active', 'black')],
              background=[('active', '#d9d9d9'), ('!active', '#f0f0f0')])

# Simulación de localStorage
class LocalStorage:
    storage = {}
    
    @staticmethod
    def set_item(key, value):
        LocalStorage.storage[key] = value
        
    @staticmethod
    def get_item(key):
        return LocalStorage.storage.get(key, None)
        
    @staticmethod
    def remove_item(key):
        if key in LocalStorage.storage:
            del LocalStorage.storage[key]

# Clases DAO (Data Access Object)
class AuthDAO:
    BASE_URL = "http://localhost:5000"
    
    @staticmethod
    def login(email, password):
        try:
            response = requests.post(
                f"{AuthDAO.BASE_URL}/login",
                json={"email": email, "password": password}
            )
            if response.status_code == 200:
                data = response.json()
                LocalStorage.set_item('access_token', data['access_token'])
                LocalStorage.set_item('refresh_token', data['refresh_token'])
                LocalStorage.set_item('user', json.dumps(data['user']))
                return data['user']
            else:
                messagebox.showerror("Error", response.json().get('error', 'Error en el login'))
                return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de conexión", str(e))
            return None
    
    @staticmethod
    def logout():
        LocalStorage.remove_item('access_token')
        LocalStorage.remove_item('refresh_token')
        LocalStorage.remove_item('user')
    
    @staticmethod
    def get_current_user():
        user_data = LocalStorage.get_item('user')
        if user_data:
            return json.loads(user_data)
        return None
    
    @staticmethod
    def recover_password(email):
        try:
            response = requests.post(
                f"{AuthDAO.BASE_URL}/recuperar-contrasena",
                json={"email": email}
            )
            if response.status_code == 200:
                return response.json()
            else:
                messagebox.showerror("Error", response.json().get('error', 'Error al recuperar contraseña'))
                return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de conexión", str(e))
            return None

class ChildDAO:
    BASE_URL = "http://localhost:5000"
    
    @staticmethod
    def get_all_children():
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                f"{ChildDAO.BASE_URL}/children",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
    
    @staticmethod
    def get_child_by_id(child_id):
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                f"{ChildDAO.BASE_URL}/child/{child_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
    
    @staticmethod
    def get_child_by_name(name):
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                f"{ChildDAO.BASE_URL}/children/{name}",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
    
    @staticmethod
    def get_child_historial(child_id):
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                f"{ChildDAO.BASE_URL}/historial/{child_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
    
    @staticmethod
    def add_historial(child_id, data, hora, estat, totalHores):
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(
                f"{ChildDAO.BASE_URL}/medicos/historial",
                json={
                    "child_id": child_id,
                    "data": data,
                    "hora": hora,
                    "estat": estat,
                    "totalHores": totalHores
                },
                headers=headers
            )
            
            if response.status_code == 201:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
    
    @staticmethod
    def add_child(name, edad, informacion_medica, tutor_id=None, cuidador_id=None):
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(
                f"{ChildDAO.BASE_URL}/children",
                json={
                    "child_name": name,
                    "edad": edad,
                    "informacioMedica": informacion_medica,
                    "tutor_id": tutor_id,
                    "cuidador_id": cuidador_id
                },
                headers=headers
            )
            
            if response.status_code == 201:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
    
    @staticmethod
    def update_child(child_id, name, edad, informacion_medica, tutor_id=None, cuidador_id=None):
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.put(
                f"{ChildDAO.BASE_URL}/children/{child_id}",
                json={
                    "child_name": name,
                    "edad": edad,
                    "informacioMedica": informacion_medica,
                    "tutor_id": tutor_id,
                    "cuidador_id": cuidador_id
                },
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
    
    @staticmethod
    def delete_child(child_id):
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.delete(
                f"{ChildDAO.BASE_URL}/children/{child_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
    
    @staticmethod
    def get_children_by_tutor(tutor_id):
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                f"{ChildDAO.BASE_URL}/tutor/{tutor_id}/children",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
    
    @staticmethod
    def get_children_by_cuidador(cuidador_id):
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                f"{ChildDAO.BASE_URL}/cuidador/{cuidador_id}/children",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None

class UserDAO:
    BASE_URL = "http://localhost:5000"
    
    @staticmethod
    def get_all_users():
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                f"{UserDAO.BASE_URL}/admin/usuarios",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
    
    @staticmethod
    def get_cuidadores():
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                f"{UserDAO.BASE_URL}/medico/cuidadores",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
    
    @staticmethod
    def get_tutores():
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                f"{UserDAO.BASE_URL}/admin/tutores",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
    
    @staticmethod
    def get_user_profile(user_id):
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                f"{UserDAO.BASE_URL}/user/{user_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
    
    @staticmethod
    def create_user(username, email, password, role_id):
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(
                f"{UserDAO.BASE_URL}/admin/usuarios",
                json={
                    "username": username,
                    "email": email,
                    "password": password,
                    "role_id": role_id
                },
                headers=headers
            )
            
            if response.status_code == 201:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
    
    @staticmethod
    def create_cuidador(username, email, password):
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(
                f"{UserDAO.BASE_URL}/admin/cuidadores",
                json={
                    "username": username,
                    "email": email,
                    "password": password
                },
                headers=headers
            )
            
            if response.status_code == 201:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
    
    @staticmethod
    def create_tutor(username, email, password):
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(
                f"{UserDAO.BASE_URL}/admin/tutores",
                json={
                    "username": username,
                    "email": email,
                    "password": password
                },
                headers=headers
            )
            
            if response.status_code == 201:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
    
    @staticmethod
    def update_user(user_id, username, email, password=None):
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            
            data = {
                "username": username,
                "email": email
            }
            
            if password:
                data["password"] = password
                
            response = requests.put(
                f"{UserDAO.BASE_URL}/admin/usuarios/{user_id}",
                json=data,
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
    
    @staticmethod
    def delete_user(user_id):
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.delete(
                f"{UserDAO.BASE_URL}/admin/usuarios/{user_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None

class CommentDAO:
    BASE_URL = "http://localhost:5000"
    
    @staticmethod
    def get_comments(child_id):
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                f"{CommentDAO.BASE_URL}/comentarios/{child_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
    
    @staticmethod
    def add_comment(child_id, text):
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(
                f"{CommentDAO.BASE_URL}/comentarios",
                json={
                    "child_id": child_id,
                    "text": text
                },
                headers=headers
            )
            
            if response.status_code == 201:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
    
    @staticmethod
    def delete_comment(comment_id):
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.delete(
                f"{CommentDAO.BASE_URL}/comentarios/{comment_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None

# Interfaz gráfica principal
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TapatApp - Gestión de Sueño Infantil")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        configure_styles()
        
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Verificar si hay un solo niño para redirigir directamente
        current_user = AuthDAO.get_current_user()
        if current_user and current_user['role_id'] == 3:  # Tutor
            children = ChildDAO.get_children_by_tutor(current_user['id'])
            if children and len(children) == 1:
                self.show_child_details(children[0]['id'])
            else:
                self.show_main_menu()
        elif current_user and current_user['role_id'] == 4:  # Cuidador
            children = ChildDAO.get_children_by_cuidador(current_user['id'])
            if children and len(children) == 1:
                self.show_child_details(children[0]['id'])
            else:
                self.show_main_menu()
        else:
            children = ChildDAO.get_all_children()
            if children and len(children) == 1:
                self.show_child_details(children[0]['id'])
            else:
                self.show_main_menu()
    
    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_main_menu(self):
        self.clear_frame()
        
        current_user = AuthDAO.get_current_user()
        
        # Header
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(
            header_frame, 
            text="TapatApp - Gestión de Sueño Infantil", 
            style="Title.TLabel"
        ).pack(side=tk.LEFT)
        
        if current_user:
            user_frame = ttk.Frame(header_frame)
            user_frame.pack(side=tk.RIGHT)
            
            ttk.Label(
                user_frame, 
                text=f"Usuario: {current_user['username']} (Rol: {self.get_role_name(current_user['role_id'])})",
                style="Header.TLabel"
            ).pack(side=tk.LEFT)
            
            ttk.Button(
                user_frame, 
                text="Mi Perfil", 
                command=self.show_user_profile
            ).pack(side=tk.LEFT, padx=5)
            
            ttk.Button(
                user_frame, 
                text="Cerrar Sesión", 
                command=self.logout
            ).pack(side=tk.LEFT, padx=5)
        
        # Main content
        content_frame = ttk.Frame(self.main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Buttons for different functionalities
        buttons = []
        
        current_user = AuthDAO.get_current_user()
        if current_user:
            # Todos pueden ver niños (pero tutores solo ven los suyos)
            buttons.append(("Gestión de Niños", self.show_children_management))
            
            # Solo admin puede ver gestión de usuarios
            if current_user['role_id'] == 1:  # Admin
                buttons.append(("Gestión de Usuarios", self.show_user_management))
                buttons.append(("Gestión de Cuidadores", self.show_cuidadores_management))
                buttons.append(("Gestión de Tutores", self.show_tutores_management))
            
            # Médicos y admin pueden ver historial
            if current_user['role_id'] in [1, 2]:  # Admin o Médico
                buttons.append(("Registrar Historial", self.show_add_historial))
            
            buttons.append(("Configuración", self.show_settings))
        
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(
                content_frame,
                text=text,
                command=command,
                width=30
            )
            btn.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
        
        # Configure grid
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        for i in range((len(buttons)+1)//2):
            content_frame.grid_rowconfigure(i, weight=1)
    
    def get_role_name(self, role_id):
        roles = {
            1: "Admin",
            2: "Médico",
            3: "Tutor",
            4: "Cuidador"
        }
        return roles.get(role_id, "Desconocido")
    
    def show_user_profile(self):
        current_user = AuthDAO.get_current_user()
        if not current_user:
            return
        
        user_data = UserDAO.get_user_profile(current_user['id'])
        if not user_data:
            messagebox.showerror("Error", "No se pudo cargar el perfil del usuario")
            return
        
        profile_window = tk.Toplevel(self.root)
        profile_window.title("Mi Perfil")
        profile_window.geometry("400x300")
        
        ttk.Label(
            profile_window,
            text="Mi Perfil",
            style="Title.TLabel"
        ).pack(pady=10)
        
        form_frame = ttk.Frame(profile_window)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Campos del formulario
        ttk.Label(form_frame, text="Nombre de usuario:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        username_entry = ttk.Entry(form_frame)
        username_entry.grid(row=0, column=1, padx=5, pady=5)
        username_entry.insert(0, user_data['username'])
        
        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        email_entry = ttk.Entry(form_frame)
        email_entry.grid(row=1, column=1, padx=5, pady=5)
        email_entry.insert(0, user_data['email'])
        
        ttk.Label(form_frame, text="Nueva contraseña:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        password_entry = ttk.Entry(form_frame, show="*")
        password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Rol:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        ttk.Label(form_frame, text=self.get_role_name(user_data['role_id'])).grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Botones
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            button_frame,
            text="Guardar Cambios",
            command=lambda: self.update_profile(
                user_data['id'],
                username_entry.get(),
                email_entry.get(),
                password_entry.get(),
                profile_window
            )
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancelar",
            command=profile_window.destroy
        ).pack(side=tk.LEFT, padx=5)
    
    def update_profile(self, user_id, username, email, password, window):
        if not username or not email:
            messagebox.showwarning("Advertencia", "Nombre de usuario y email son obligatorios")
            return
        
        result = UserDAO.update_user(user_id, username, email, password if password else None)
        if result:
            messagebox.showinfo("Éxito", "Perfil actualizado correctamente")
            # Actualizar datos en localStorage
            current_user = AuthDAO.get_current_user()
            if current_user:
                current_user['username'] = username
                current_user['email'] = email
                LocalStorage.set_item('user', json.dumps(current_user))
            window.destroy()
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el perfil")
    
    def logout(self):
        AuthDAO.logout()
        self.root.destroy()
        show_login_window()
    
    def show_children_management(self):
        self.clear_frame()
        
        # Header
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(
            header_frame, 
            text="Gestión de Niños", 
            style="Title.TLabel"
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            header_frame, 
            text="Volver", 
            command=self.show_main_menu
        ).pack(side=tk.RIGHT)
        
        # Search frame
        search_frame = ttk.Frame(self.main_frame)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(search_frame, text="Buscar niño:").pack(side=tk.LEFT)
        self.child_search_entry = ttk.Entry(search_frame, width=30)
        self.child_search_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            search_frame,
            text="Buscar",
            command=self.search_child
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            search_frame,
            text="Mostrar Todos",
            command=self.show_all_children
        ).pack(side=tk.LEFT, padx=5)
        
        # Children list
        list_frame = ttk.Frame(self.main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("id", "name", "age", "medical_info", "tutor", "cuidador")
        self.children_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings"
        )
        
        self.children_tree.heading("id", text="ID")
        self.children_tree.heading("name", text="Nombre")
        self.children_tree.heading("age", text="Edad")
        self.children_tree.heading("medical_info", text="Información Médica")
        self.children_tree.heading("tutor", text="Tutor")
        self.children_tree.heading("cuidador", text="Cuidador")
        
        self.children_tree.column("id", width=50, anchor=tk.CENTER)
        self.children_tree.column("name", width=150)
        self.children_tree.column("age", width=50, anchor=tk.CENTER)
        self.children_tree.column("medical_info", width=200)
        self.children_tree.column("tutor", width=150)
        self.children_tree.column("cuidador", width=150)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.children_tree.yview)
        self.children_tree.configure(yscroll=scrollbar.set)
        
        self.children_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons
        action_frame = ttk.Frame(self.main_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            action_frame,
            text="Ver Detalles",
            command=self.show_selected_child_details
        ).pack(side=tk.LEFT, padx=5)
        
        # Solo admin puede agregar/editar/eliminar niños
        current_user = AuthDAO.get_current_user()
        if current_user and current_user['role_id'] == 1:  # Admin
            ttk.Button(
                action_frame,
                text="Agregar Niño",
                command=self.show_add_child_form
            ).pack(side=tk.LEFT, padx=5)
            
            ttk.Button(
                action_frame,
                text="Editar",
                command=self.show_edit_child_form
            ).pack(side=tk.LEFT, padx=5)
            
            ttk.Button(
                action_frame,
                text="Eliminar",
                command=self.delete_child
            ).pack(side=tk.LEFT, padx=5)
        
        # Load initial data
        self.show_all_children()
    
    def search_child(self):
        name = self.child_search_entry.get()
        if not name:
            messagebox.showwarning("Advertencia", "Por favor ingrese un nombre para buscar")
            return
        
        child = ChildDAO.get_child_by_name(name)
        if child:
            self.children_tree.delete(*self.children_tree.get_children())
            tutor_name = self.get_user_name(child.get('tutor_id'))
            cuidador_name = self.get_user_name(child.get('cuidador_id'))
            
            self.children_tree.insert("", tk.END, values=(
                child.get('id'),
                child.get('child_name'),
                child.get('edad', 'N/A'),
                child.get('informacioMedica', 'N/A'),
                tutor_name,
                cuidador_name
            ))
    
    def get_user_name(self, user_id):
        if not user_id:
            return "No asignado"
        
        current_user = AuthDAO.get_current_user()
        if current_user and current_user['id'] == user_id:
            return current_user['username']
        
        user = UserDAO.get_user_profile(user_id)
        if user:
            return user['username']
        return "Desconocido"
    
    def show_all_children(self):
        current_user = AuthDAO.get_current_user()
        if not current_user:
            return
        
        if current_user['role_id'] == 3:  # Tutor
            children = ChildDAO.get_children_by_tutor(current_user['id'])
        elif current_user['role_id'] == 4:  # Cuidador
            children = ChildDAO.get_children_by_cuidador(current_user['id'])
        else:
            children = ChildDAO.get_all_children()
            
        if children:
            self.children_tree.delete(*self.children_tree.get_children())
            for child in children:
                tutor_name = self.get_user_name(child.get('tutor_id'))
                cuidador_name = self.get_user_name(child.get('cuidador_id'))
                
                self.children_tree.insert("", tk.END, values=(
                    child.get('id'),
                    child.get('child_name'),
                    child.get('edad', 'N/A'),
                    child.get('informacioMedica', 'N/A'),
                    tutor_name,
                    cuidador_name
                ))
    
    def show_selected_child_details(self):
        selected_item = self.children_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione un niño")
            return
        
        item = self.children_tree.item(selected_item[0])
        child_id = item['values'][0]
        self.show_child_details(child_id)
    
    def show_child_details(self, child_id):
        self.clear_frame()
        
        # Obtener datos del niño
        child = ChildDAO.get_child_by_id(child_id)
        if not child:
            messagebox.showerror("Error", "Niño no encontrado")
            self.show_children_management()
            return
        
        # Header
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(
            header_frame, 
            text=f"Detalles de {child['child_name']}", 
            style="Title.TLabel"
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            header_frame, 
            text="Volver", 
            command=self.show_children_management
        ).pack(side=tk.RIGHT)
        
        # Notebook para pestañas
        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña de información general
        info_frame = ttk.Frame(notebook)
        notebook.add(info_frame, text="Información General")
        
        # Mostrar información básica
        tutor_name = self.get_user_name(child.get('tutor_id'))
        cuidador_name = self.get_user_name(child.get('cuidador_id'))
        
        info_text = f"Nombre: {child['child_name']}\n"
        info_text += f"Edad: {child.get('edad', 'N/A')}\n"
        info_text += f"Información Médica: {child.get('informacioMedica', 'N/A')}\n"
        info_text += f"Tutor: {tutor_name}\n"
        info_text += f"Cuidador: {cuidador_name}\n"
        
        ttk.Label(info_frame, text=info_text).pack(pady=20, padx=20, anchor=tk.W)
        
        # Pestaña de historial de sueño
        historial_frame = ttk.Frame(notebook)
        notebook.add(historial_frame, text="Historial de Sueño")
        self.setup_historial_tab(historial_frame, child_id)
        
        # Pestaña de comentarios
        comments_frame = ttk.Frame(notebook)
        notebook.add(comments_frame, text="Comentarios")
        self.setup_comments_tab(comments_frame, child_id)
    
    def setup_historial_tab(self, parent_frame, child_id):
        # Treeview para mostrar historial
        columns = ("fecha", "hora", "estado", "horas_sueño")
        self.historial_tree = ttk.Treeview(
            parent_frame,
            columns=columns,
            show="headings"
        )
        
        self.historial_tree.heading("fecha", text="Fecha")
        self.historial_tree.heading("hora", text="Hora")
        self.historial_tree.heading("estado", text="Estado")
        self.historial_tree.heading("horas_sueño", text="Horas de Sueño")
        
        for col in columns:
            self.historial_tree.column(col, width=120, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(parent_frame, orient=tk.VERTICAL, command=self.historial_tree.yview)
        self.historial_tree.configure(yscroll=scrollbar.set)
        
        self.historial_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Cargar datos
        historial = ChildDAO.get_child_historial(child_id)
        if historial:
            for entry in historial:
                self.historial_tree.insert("", tk.END, values=(
                    entry.get('data'),
                    entry.get('hora'),
                    entry.get('estat'),
                    entry.get('totalHores')
                ))
    
    def setup_comments_tab(self, parent_frame, child_id):
        # Frame para lista de comentarios
        list_frame = ttk.Frame(parent_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("id", "usuario", "texto", "fecha")
        self.comments_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings"
        )
        
        self.comments_tree.heading("id", text="ID")
        self.comments_tree.heading("usuario", text="Usuario")
        self.comments_tree.heading("texto", text="Comentario")
        self.comments_tree.heading("fecha", text="Fecha")
        
        self.comments_tree.column("id", width=50, anchor=tk.CENTER)
        self.comments_tree.column("usuario", width=100)
        self.comments_tree.column("texto", width=300)
        self.comments_tree.column("fecha", width=120)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.comments_tree.yview)
        self.comments_tree.configure(yscroll=scrollbar.set)
        
        self.comments_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame para agregar comentario
        add_frame = ttk.Frame(parent_frame)
        add_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(add_frame, text="Nuevo comentario:").pack(side=tk.LEFT)
        self.new_comment_entry = ttk.Entry(add_frame, width=50)
        self.new_comment_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            add_frame,
            text="Agregar",
            command=lambda: self.add_comment(child_id)
        ).pack(side=tk.LEFT)
        
        # Botón para eliminar comentario
        current_user = AuthDAO.get_current_user()
        if current_user and current_user['role_id'] in [1, 2]:  # Solo admin y médicos pueden eliminar
            ttk.Button(
                parent_frame,
                text="Eliminar Comentario Seleccionado",
                command=self.delete_selected_comment
            ).pack(pady=5)
        
        # Cargar comentarios
        self.load_comments(child_id)
    
    def load_comments(self, child_id):
        comments = CommentDAO.get_comments(child_id)
        if comments:
            self.comments_tree.delete(*self.comments_tree.get_children())
            for comment in comments:
                username = self.get_user_name(comment.get('user_id'))
                self.comments_tree.insert("", tk.END, values=(
                    comment.get('id'),
                    username,
                    comment.get('text'),
                    comment.get('timestamp')
                ))
    
    def add_comment(self, child_id):
        text = self.new_comment_entry.get()
        if not text:
            messagebox.showwarning("Advertencia", "Por favor escriba un comentario")
            return
        
        result = CommentDAO.add_comment(child_id, text)
        if result:
            messagebox.showinfo("Éxito", "Comentario agregado correctamente")
            self.new_comment_entry.delete(0, tk.END)
            self.load_comments(child_id)
        else:
            messagebox.showerror("Error", "No se pudo agregar el comentario")
    
    def delete_selected_comment(self):
        selected_item = self.comments_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione un comentario")
            return
        
        comment_id = self.comments_tree.item(selected_item[0])['values'][0]
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este comentario?"):
            result = CommentDAO.delete_comment(comment_id)
            if result:
                messagebox.showinfo("Éxito", "Comentario eliminado correctamente")
                self.comments_tree.delete(selected_item)
            else:
                messagebox.showerror("Error", "No se pudo eliminar el comentario")
    
    def show_add_child_form(self):
        form_window = tk.Toplevel(self.root)
        form_window.title("Agregar Niño")
        form_window.geometry("500x400")
        
        ttk.Label(form_window, text="Agregar Niño", style="Title.TLabel").pack(pady=10)
        
        form_frame = ttk.Frame(form_window)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Campos del formulario
        ttk.Label(form_frame, text="Nombre del niño:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        name_entry = ttk.Entry(form_frame)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Edad:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        age_entry = ttk.Entry(form_frame)
        age_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Información médica:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        medical_info_entry = ttk.Entry(form_frame)
        medical_info_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Obtener tutores y cuidadores
        tutores = UserDAO.get_tutores()
        cuidadores = UserDAO.get_cuidadores()
        
        ttk.Label(form_frame, text="Tutor:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        tutor_combobox = ttk.Combobox(form_frame, state="readonly")
        tutor_combobox.grid(row=3, column=1, padx=5, pady=5)
        
        if tutores:
            tutor_combobox['values'] = [(t['id'], t['username']) for t in tutores]
            if tutores:
                tutor_combobox.current(0)
        
        ttk.Label(form_frame, text="Cuidador:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        cuidador_combobox = ttk.Combobox(form_frame, state="readonly")
        cuidador_combobox.grid(row=4, column=1, padx=5, pady=5)
        
        if cuidadores:
            cuidador_combobox['values'] = [(c['id'], c['username']) for c in cuidadores]
            if cuidadores:
                cuidador_combobox.current(0)
        
        # Botones
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            button_frame,
            text="Guardar",
            command=lambda: self.save_child(
                name_entry.get(),
                age_entry.get(),
                medical_info_entry.get(),
                tutor_combobox.get().split(",")[0].strip("(") if tutor_combobox.get() else None,
                cuidador_combobox.get().split(",")[0].strip("(") if cuidador_combobox.get() else None,
                form_window
            )
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancelar",
            command=form_window.destroy
        ).pack(side=tk.LEFT, padx=5)
    
    def save_child(self, name, age, medical_info, tutor_id, cuidador_id, window):
        if not name:
            messagebox.showwarning("Advertencia", "El nombre del niño es obligatorio")
            return
        
        result = ChildDAO.add_child(name, age, medical_info, tutor_id, cuidador_id)
        if result:
            messagebox.showinfo("Éxito", "Niño agregado correctamente")
            window.destroy()
            self.show_all_children()
        else:
            messagebox.showerror("Error", "No se pudo agregar el niño")
    
    def show_edit_child_form(self):
        selected_item = self.children_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione un niño")
            return
        
        item = self.children_tree.item(selected_item[0])
        child_id = item['values'][0]
        
        child = ChildDAO.get_child_by_id(child_id)
        if not child:
            messagebox.showerror("Error", "No se pudo cargar la información del niño")
            return
        
        form_window = tk.Toplevel(self.root)
        form_window.title("Editar Niño")
        form_window.geometry("500x400")
        
        ttk.Label(form_window, text="Editar Niño", style="Title.TLabel").pack(pady=10)
        
        form_frame = ttk.Frame(form_window)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Campos del formulario
        ttk.Label(form_frame, text="Nombre del niño:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        name_entry = ttk.Entry(form_frame)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        name_entry.insert(0, child.get('child_name', ''))
        
        ttk.Label(form_frame, text="Edad:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        age_entry = ttk.Entry(form_frame)
        age_entry.grid(row=1, column=1, padx=5, pady=5)
        age_entry.insert(0, child.get('edad', ''))
        
        ttk.Label(form_frame, text="Información médica:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        medical_info_entry = ttk.Entry(form_frame)
        medical_info_entry.grid(row=2, column=1, padx=5, pady=5)
        medical_info_entry.insert(0, child.get('informacioMedica', ''))
        
        # Obtener tutores y cuidadores
        tutores = UserDAO.get_tutores()
        cuidadores = UserDAO.get_cuidadores()
        
        ttk.Label(form_frame, text="Tutor:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        tutor_combobox = ttk.Combobox(form_frame, state="readonly")
        tutor_combobox.grid(row=3, column=1, padx=5, pady=5)
        
        if tutores:
            tutor_values = [(t['id'], t['username']) for t in tutores]
            tutor_combobox['values'] = tutor_values
            
            # Seleccionar el tutor actual si existe
            current_tutor_id = child.get('tutor_id')
            if current_tutor_id:
                for i, (t_id, t_name) in enumerate(tutor_values):
                    if str(t_id) == str(current_tutor_id):
                        tutor_combobox.current(i)
                        break
            elif tutor_values:
                tutor_combobox.current(0)
        
        ttk.Label(form_frame, text="Cuidador:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        cuidador_combobox = ttk.Combobox(form_frame, state="readonly")
        cuidador_combobox.grid(row=4, column=1, padx=5, pady=5)
        
        if cuidadores:
            cuidador_values = [(c['id'], c['username']) for c in cuidadores]
            cuidador_combobox['values'] = cuidador_values
            
            # Seleccionar el cuidador actual si existe
            current_cuidador_id = child.get('cuidador_id')
            if current_cuidador_id:
                for i, (c_id, c_name) in enumerate(cuidador_values):
                    if str(c_id) == str(current_cuidador_id):
                        cuidador_combobox.current(i)
                        break
            elif cuidador_values:
                cuidador_combobox.current(0)
        
        # Botones
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            button_frame,
            text="Guardar",
            command=lambda: self.update_child(
                child_id,
                name_entry.get(),
                age_entry.get(),
                medical_info_entry.get(),
                tutor_combobox.get().split(",")[0].strip("(") if tutor_combobox.get() else None,
                cuidador_combobox.get().split(",")[0].strip("(") if cuidador_combobox.get() else None,
                form_window
            )
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancelar",
            command=form_window.destroy
        ).pack(side=tk.LEFT, padx=5)
    
    def update_child(self, child_id, name, age, medical_info, tutor_id, cuidador_id, window):
        if not name:
            messagebox.showwarning("Advertencia", "El nombre del niño es obligatorio")
            return
        
        result = ChildDAO.update_child(child_id, name, age, medical_info, tutor_id, cuidador_id)
        if result:
            messagebox.showinfo("Éxito", "Niño actualizado correctamente")
            window.destroy()
            self.show_all_children()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el niño")
    
    def delete_child(self):
        selected_item = self.children_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione un niño")
            return
        
        child_id = self.children_tree.item(selected_item[0])['values'][0]
        child_name = self.children_tree.item(selected_item[0])['values'][1]
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar al niño {child_name}?"):
            result = ChildDAO.delete_child(child_id)
            if result:
                messagebox.showinfo("Éxito", "Niño eliminado correctamente")
                self.show_all_children()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el niño")
    
    def show_add_historial(self):
        self.clear_frame()
        
        # Header
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(
            header_frame, 
            text="Registrar Historial de Sueño", 
            style="Title.TLabel"
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            header_frame, 
            text="Volver", 
            command=self.show_main_menu
        ).pack(side=tk.RIGHT)
        
        # Formulario
        form_frame = ttk.Frame(self.main_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Selección de niño
        ttk.Label(form_frame, text="Niño:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.historial_child_combobox = ttk.Combobox(form_frame, state="readonly")
        self.historial_child_combobox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Cargar niños en el combobox
        children = ChildDAO.get_all_children()
        if children:
            self.historial_child_combobox['values'] = [(child['id'], child['child_name']) for child in children]
            self.historial_child_combobox.current(0)
        
        # Fecha
        ttk.Label(form_frame, text="Fecha (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.historial_date_entry = ttk.Entry(form_frame)
        self.historial_date_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.historial_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Hora
        ttk.Label(form_frame, text="Hora (HH:MM):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.historial_time_entry = ttk.Entry(form_frame)
        self.historial_time_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.historial_time_entry.insert(0, datetime.now().strftime("%H:%M"))
        
        # Estado
        ttk.Label(form_frame, text="Estado:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.historial_state_combobox = ttk.Combobox(form_frame, values=["Dormido", "Despierto", "Inquieto"])
        self.historial_state_combobox.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.historial_state_combobox.current(0)
        
        # Horas de sueño
        ttk.Label(form_frame, text="Horas de sueño:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.historial_hours_entry = ttk.Entry(form_frame)
        self.historial_hours_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Botón para guardar
        ttk.Button(
            form_frame,
            text="Guardar Historial",
            command=self.save_historial
        ).grid(row=5, column=1, pady=10, sticky=tk.E)
    
    def save_historial(self):
        # Validar datos
        child_id = self.historial_child_combobox.get().split(",")[0].strip("(")
        date = self.historial_date_entry.get()
        time = self.historial_time_entry.get()
        state = self.historial_state_combobox.get()
        hours = self.historial_hours_entry.get()
        
        if not all([child_id, date, time, state, hours]):
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
            return
        
        # Guardar historial
        result = ChildDAO.add_historial(child_id, date, time, state, hours)
        if result:
            messagebox.showinfo("Éxito", "Historial guardado correctamente")
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "No se pudo guardar el historial")
    
    def show_user_management(self):
        self.clear_frame()
        
        # Verificar permisos de administrador
        current_user = AuthDAO.get_current_user()
        if not current_user or current_user['role_id'] != 1:  # 1 = Admin
            messagebox.showerror("Error", "No tiene permisos para acceder a esta sección")
            self.show_main_menu()
            return
        
        # Header
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(
            header_frame, 
            text="Gestión de Usuarios", 
            style="Title.TLabel"
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            header_frame, 
            text="Volver", 
            command=self.show_main_menu
        ).pack(side=tk.RIGHT)
        
        # Users list
        list_frame = ttk.Frame(self.main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("id", "username", "email", "role_id")
        self.users_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings"
        )
        
        self.users_tree.heading("id", text="ID")
        self.users_tree.heading("username", text="Nombre de Usuario")
        self.users_tree.heading("email", text="Email")
        self.users_tree.heading("role_id", text="Rol")
        
        self.users_tree.column("id", width=50, anchor=tk.CENTER)
        self.users_tree.column("username", width=150)
        self.users_tree.column("email", width=200)
        self.users_tree.column("role_id", width=100)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.users_tree.yview)
        self.users_tree.configure(yscroll=scrollbar.set)
        
        self.users_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons
        action_frame = ttk.Frame(self.main_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            action_frame,
            text="Actualizar Lista",
            command=self.load_users
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="Agregar Usuario",
            command=self.show_add_user_form
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="Editar Usuario",
            command=self.show_edit_user_form
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="Eliminar Usuario",
            command=self.delete_user
        ).pack(side=tk.LEFT, padx=5)
        
        # Load initial data
        self.load_users()
    
    def show_cuidadores_management(self):
        self.clear_frame()
        
        # Verificar permisos de administrador
        current_user = AuthDAO.get_current_user()
        if not current_user or current_user['role_id'] != 1:  # 1 = Admin
            messagebox.showerror("Error", "No tiene permisos para acceder a esta sección")
            self.show_main_menu()
            return
        
        # Header
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(
            header_frame, 
            text="Gestión de Cuidadores", 
            style="Title.TLabel"
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            header_frame, 
            text="Volver", 
            command=self.show_main_menu
        ).pack(side=tk.RIGHT)
        
        # Cuidadores list
        list_frame = ttk.Frame(self.main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("id", "username", "email")
        self.cuidadores_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings"
        )
        
        self.cuidadores_tree.heading("id", text="ID")
        self.cuidadores_tree.heading("username", text="Nombre de Usuario")
        self.cuidadores_tree.heading("email", text="Email")
        
        self.cuidadores_tree.column("id", width=50, anchor=tk.CENTER)
        self.cuidadores_tree.column("username", width=150)
        self.cuidadores_tree.column("email", width=200)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.cuidadores_tree.yview)
        self.cuidadores_tree.configure(yscroll=scrollbar.set)
        
        self.cuidadores_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons
        action_frame = ttk.Frame(self.main_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            action_frame,
            text="Actualizar Lista",
            command=self.load_cuidadores
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="Agregar Cuidador",
            command=self.show_add_cuidador_form
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="Eliminar Cuidador",
            command=self.delete_cuidador
        ).pack(side=tk.LEFT, padx=5)
        
        # Load initial data
        self.load_cuidadores()
    
    def show_tutores_management(self):
        self.clear_frame()
        
        # Verificar permisos de administrador
        current_user = AuthDAO.get_current_user()
        if not current_user or current_user['role_id'] != 1:  # 1 = Admin
            messagebox.showerror("Error", "No tiene permisos para acceder a esta sección")
            self.show_main_menu()
            return
        
        # Header
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(
            header_frame, 
            text="Gestión de Tutores", 
            style="Title.TLabel"
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            header_frame, 
            text="Volver", 
            command=self.show_main_menu
        ).pack(side=tk.RIGHT)
        
        # Tutores list
        list_frame = ttk.Frame(self.main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("id", "username", "email")
        self.tutores_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings"
        )
        
        self.tutores_tree.heading("id", text="ID")
        self.tutores_tree.heading("username", text="Nombre de Usuario")
        self.tutores_tree.heading("email", text="Email")
        
        self.tutores_tree.column("id", width=50, anchor=tk.CENTER)
        self.tutores_tree.column("username", width=150)
        self.tutores_tree.column("email", width=200)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tutores_tree.yview)
        self.tutores_tree.configure(yscroll=scrollbar.set)
        
        self.tutores_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons
        action_frame = ttk.Frame(self.main_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            action_frame,
            text="Actualizar Lista",
            command=self.load_tutores
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="Agregar Tutor",
            command=self.show_add_tutor_form
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="Eliminar Tutor",
            command=self.delete_tutor
        ).pack(side=tk.LEFT, padx=5)
        
        # Load initial data
        self.load_tutores()
    
    def load_users(self):
        users = UserDAO.get_all_users()
        if users:
            self.users_tree.delete(*self.users_tree.get_children())
            for user in users:
                self.users_tree.insert("", tk.END, values=(
                    user.get('id'),
                    user.get('username'),
                    user.get('email'),
                    self.get_role_name(user.get('role_id'))
                ))
    
    def load_cuidadores(self):
        cuidadores = UserDAO.get_cuidadores()
        if cuidadores:
            self.cuidadores_tree.delete(*self.cuidadores_tree.get_children())
            for cuidador in cuidadores:
                self.cuidadores_tree.insert("", tk.END, values=(
                    cuidador.get('id'),
                    cuidador.get('username'),
                    cuidador.get('email')
                ))
    
    def load_tutores(self):
        tutores = UserDAO.get_tutores()
        if tutores:
            self.tutores_tree.delete(*self.tutores_tree.get_children())
            for tutor in tutores:
                self.tutores_tree.insert("", tk.END, values=(
                    tutor.get('id'),
                    tutor.get('username'),
                    tutor.get('email')
                ))
    
    def show_add_user_form(self):
        self.show_user_form("Agregar Usuario")
    
    def show_add_cuidador_form(self):
        self.show_user_form("Agregar Cuidador", is_cuidador=True)
    
    def show_add_tutor_form(self):
        self.show_user_form("Agregar Tutor", is_tutor=True)
    
    def show_user_form(self, title, is_cuidador=False, is_tutor=False):
        form_window = tk.Toplevel(self.root)
        form_window.title(title)
        form_window.geometry("400x300")
        
        ttk.Label(form_window, text=title, style="Title.TLabel").pack(pady=10)
        
        form_frame = ttk.Frame(form_window)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Campos del formulario
        ttk.Label(form_frame, text="Nombre de usuario:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        username_entry = ttk.Entry(form_frame)
        username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        email_entry = ttk.Entry(form_frame)
        email_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Contraseña:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        password_entry = ttk.Entry(form_frame, show="*")
        password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        if not is_cuidador and not is_tutor:
            ttk.Label(form_frame, text="Rol:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
            role_combobox = ttk.Combobox(form_frame, values=["1 - Admin", "2 - Médico", "3 - Tutor", "4 - Cuidador"])
            role_combobox.grid(row=3, column=1, padx=5, pady=5)
            role_combobox.current(0)
        
        # Botones
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            button_frame,
            text="Guardar",
            command=lambda: self.save_user(
                username_entry.get(),
                email_entry.get(),
                password_entry.get(),
                role_combobox.get().split(" - ")[0] if not is_cuidador and not is_tutor else "4" if is_cuidador else "3",
                is_cuidador,
                is_tutor,
                form_window
            )
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancelar",
            command=form_window.destroy
        ).pack(side=tk.LEFT, padx=5)
    
    def save_user(self, username, email, password, role_id, is_cuidador, is_tutor, form_window):
        if not all([username, email, password]):
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
            return
        
        if is_cuidador:
            result = UserDAO.create_cuidador(username, email, password)
        elif is_tutor:
            result = UserDAO.create_tutor(username, email, password)
        else:
            result = UserDAO.create_user(username, email, password, role_id)
        
        if result:
            messagebox.showinfo("Éxito", "Usuario guardado correctamente")
            form_window.destroy()
            if is_cuidador:
                self.load_cuidadores()
            elif is_tutor:
                self.load_tutores()
            else:
                self.load_users()
        else:
            messagebox.showerror("Error", "No se pudo guardar el usuario")
    
    def show_edit_user_form(self):
        selected_item = self.users_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione un usuario")
            return
        
        user_data = self.users_tree.item(selected_item[0])['values']
        
        form_window = tk.Toplevel(self.root)
        form_window.title("Editar Usuario")
        form_window.geometry("400x300")
        
        ttk.Label(form_window, text="Editar Usuario", style="Title.TLabel").pack(pady=10)
        
        form_frame = ttk.Frame(form_window)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Campos del formulario
        ttk.Label(form_frame, text="Nombre de usuario:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        username_entry = ttk.Entry(form_frame)
        username_entry.grid(row=0, column=1, padx=5, pady=5)
        username_entry.insert(0, user_data[1])
        
        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        email_entry = ttk.Entry(form_frame)
        email_entry.grid(row=1, column=1, padx=5, pady=5)
        email_entry.insert(0, user_data[2])
        
        ttk.Label(form_frame, text="Nueva contraseña:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        password_entry = ttk.Entry(form_frame, show="*")
        password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Rol:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        role_combobox = ttk.Combobox(form_frame, values=["1 - Admin", "2 - Médico", "3 - Tutor", "4 - Cuidador"])
        role_combobox.grid(row=3, column=1, padx=5, pady=5)
        
        # Establecer el rol actual
        current_role = user_data[3]
        role_combobox.set(f"{current_role.split(' - ')[0]} - {current_role.split(' - ')[1]}")
        
        # Botones
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            button_frame,
            text="Guardar",
            command=lambda: self.update_user(
                user_data[0],
                username_entry.get(),
                email_entry.get(),
                password_entry.get(),
                role_combobox.get().split(" - ")[0],
                form_window
            )
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancelar",
            command=form_window.destroy
        ).pack(side=tk.LEFT, padx=5)
    
    def update_user(self, user_id, username, email, password, role_id, form_window):
        if not all([username, email]):
            messagebox.showwarning("Advertencia", "Nombre de usuario y email son obligatorios")
            return
        
        result = UserDAO.update_user(user_id, username, email, password if password else None)
        if result:
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
            form_window.destroy()
            self.load_users()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el usuario")
    
    def delete_user(self):
        selected_item = self.users_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione un usuario")
            return
        
        user_data = self.users_tree.item(selected_item[0])['values']
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar al usuario {user_data[1]}?"):
            result = UserDAO.delete_user(user_data[0])
            if result:
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
                self.load_users()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el usuario")
    
    def delete_cuidador(self):
        selected_item = self.cuidadores_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione un cuidador")
            return
        
        cuidador_data = self.cuidadores_tree.item(selected_item[0])['values']
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar al cuidador {cuidador_data[1]}?"):
            result = UserDAO.delete_user(cuidador_data[0])
            if result:
                messagebox.showinfo("Éxito", "Cuidador eliminado correctamente")
                self.load_cuidadores()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el cuidador")
    
    def delete_tutor(self):
        selected_item = self.tutores_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione un tutor")
            return
        
        tutor_data = self.tutores_tree.item(selected_item[0])['values']
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar al tutor {tutor_data[1]}?"):
            result = UserDAO.delete_user(tutor_data[0])
            if result:
                messagebox.showinfo("Éxito", "Tutor eliminado correctamente")
                self.load_tutores()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el tutor")
    
    def show_settings(self):
        self.clear_frame()
        
        # Header
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(
            header_frame, 
            text="Configuración", 
            style="Title.TLabel"
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            header_frame, 
            text="Volver", 
            command=self.show_main_menu
        ).pack(side=tk.RIGHT)
        
        # Contenido
        content_frame = ttk.Frame(self.main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Opción para recuperar contraseña
        ttk.Label(
            content_frame,
            text="Recuperar Contraseña",
            style="Header.TLabel"
        ).pack(pady=10)
        
        recovery_frame = ttk.Frame(content_frame)
        recovery_frame.pack(pady=10)
        
        ttk.Label(recovery_frame, text="Email:").pack(side=tk.LEFT)
        self.recovery_email_entry = ttk.Entry(recovery_frame, width=30)
        self.recovery_email_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            recovery_frame,
            text="Enviar",
            command=self.recover_password
        ).pack(side=tk.LEFT)

# Ventana de Login
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("TapatApp - Iniciar Sesión")
        self.root.geometry("400x300")
        
        configure_styles()
        
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(
            self.main_frame,
            text="Iniciar Sesión",
            style="Title.TLabel"
        ).pack(pady=20)
        
        # Formulario
        form_frame = ttk.Frame(self.main_frame)
        form_frame.pack(pady=20)
        
        ttk.Label(form_frame, text="Email:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.email_entry = ttk.Entry(form_frame, width=30)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Contraseña:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.password_entry = ttk.Entry(form_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Botones
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(
            button_frame,
            text="Iniciar Sesión",
            command=self.do_login
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            button_frame,
            text="Recuperar Contraseña",
            command=self.show_recovery
        ).pack(side=tk.LEFT, padx=10)
    
    def do_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showwarning("Advertencia", "Por favor ingrese email y contraseña")
            return
        
        user = AuthDAO.login(email, password)
        if user:
            self.root.destroy()
            root = tk.Tk()
            app = MainApp(root)
            root.mainloop()
    
    def show_recovery(self):
        recovery_window = tk.Toplevel(self.root)
        recovery_window.title("Recuperar Contraseña")
        recovery_window.geometry("400x200")
        
        ttk.Label(
            recovery_window,
            text="Recuperar Contraseña",
            style="Title.TLabel"
        ).pack(pady=20)
        
        form_frame = ttk.Frame(recovery_window)
        form_frame.pack(pady=20)
        
        ttk.Label(form_frame, text="Email:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        email_entry = ttk.Entry(form_frame, width=30)
        email_entry.grid(row=0, column=1, padx=5, pady=5)
        
        button_frame = ttk.Frame(recovery_window)
        button_frame.pack(pady=10)
        
        ttk.Button(
            button_frame,
            text="Enviar",
            command=lambda: self.send_recovery(email_entry.get(), recovery_window)
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            button_frame,
            text="Cancelar",
            command=recovery_window.destroy
        ).pack(side=tk.LEFT, padx=10)
    
    def send_recovery(self, email, window):
        if not email:
            messagebox.showwarning("Advertencia", "Por favor ingrese un email")
            return
        
        result = AuthDAO.recover_password(email)
        if result:
            messagebox.showinfo("Éxito", result.get('message', 'Se ha enviado un correo con instrucciones'))
            window.destroy()
        else:
            messagebox.showerror("Error", "No se pudo enviar el correo de recuperación")

# Función para mostrar la ventana de login
def show_login_window():
    root = tk.Tk()
    login_window = LoginWindow(root)
    root.mainloop()

# Función principal
if __name__ == "__main__":
    show_login_window()
