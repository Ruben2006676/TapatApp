import tkinter as tk
from tkinter import ttk, messagebox
import json
import requests
from datetime import datetime

# Configuración de estilos
def configure_styles():
    style = ttk.Style()
    style.configure('TFrame', background='#2E2E2E')
    style.configure('TLabel', background='#2E2E2E', foreground='white', font=('Arial', 10))
    style.configure('TButton', font=('Arial', 10), padding=5, background='#4A4A4A')
    style.configure('TEntry', font=('Arial', 10), fieldbackground='#4A4A4A')
    style.configure('Header.TLabel', font=('Arial', 12, 'bold'), foreground='#FFD700')
    style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#FFD700')
    style.configure('TNotebook', background='#2E2E2E')
    style.configure('TNotebook.Tab', padding=[10, 5], background='#4A4A4A', foreground='white')
    style.map('TButton', 
              foreground=[('active', 'white'), ('!active', 'white')],
              background=[('active', '#6B6B6B'), ('!active', '#4A4A4A')])

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

# Clases DAO
class AuthDAO:
    BASE_URL = "http://localhost:5000"
    
    @staticmethod
    def login(username, password):
        try:
            response = requests.post(
                f"{AuthDAO.BASE_URL}/login",
                json={"username": username, "password": password}
            )
            if response.status_code == 200:
                data = response.json()
                LocalStorage.set_item('access_token', data['access_token'])
                LocalStorage.set_item('user', json.dumps(data['user']))
                return data['user']
            else:
                messagebox.showerror("Error", response.json().get('error', 'Error en el login'))
                return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de conexión", str(e))
            return None

class CharacterDAO:
    BASE_URL = "http://localhost:5000"
    
    @staticmethod
    def create_character(name, race, char_class):
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(
                f"{CharacterDAO.BASE_URL}/characters",
                json={
                    "name": name,
                    "race": race,
                    "class": char_class
                },
                headers=headers
            )
            return response.json() if response.status_code == 201 else None
        except requests.exceptions.RequestException:
            return None
    
    @staticmethod
    def get_characters():
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                f"{CharacterDAO.BASE_URL}/characters",
                headers=headers
            )
            return response.json()['characters'] if response.status_code == 200 else []
        except requests.exceptions.RequestException:
            return []

class GameSessionDAO:
    BASE_URL = "http://localhost:5000"
    
    @staticmethod
    def create_session(adventure_id):
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(
                f"{GameSessionDAO.BASE_URL}/game_sessions",
                json={"adventure_id": adventure_id},
                headers=headers
            )
            return response.json() if response.status_code == 201 else None
        except requests.exceptions.RequestException:
            return None
    
    @staticmethod
    def join_session(session_id, character_id):
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(
                f"{GameSessionDAO.BASE_URL}/game_sessions/{session_id}/join",
                json={"character_id": character_id},
                headers=headers
            )
            return response.json() if response.status_code == 200 else None
        except requests.exceptions.RequestException:
            return None

class CombatDAO:
    BASE_URL = "http://localhost:5000"
    
    @staticmethod
    def start_combat(session_id):
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(
                f"{CombatDAO.BASE_URL}/combat/{session_id}/start",
                headers=headers
            )
            return response.json() if response.status_code == 200 else None
        except requests.exceptions.RequestException:
            return None

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RolPlayer")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        configure_styles()
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.show_main_menu()
    
    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_main_menu(self):
        self.clear_frame()
        current_user = json.loads(LocalStorage.get_item('user')) if LocalStorage.get_item('user') else None
        
        # Header
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header_frame, text="RolPlayer", style="Title.TLabel").pack(side=tk.LEFT)
        
        if current_user:
            user_frame = ttk.Frame(header_frame)
            user_frame.pack(side=tk.RIGHT)
            
            ttk.Label(user_frame, 
                     text=f"Usuario: {current_user['id']} (Rol: {current_user['role']})",
                     style="Header.TLabel").pack(side=tk.LEFT)
            
            ttk.Button(user_frame, text="Cerrar Sesión", command=self.logout).pack(side=tk.LEFT, padx=5)
        
        # Contenido principal
        content_frame = ttk.Frame(self.main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        buttons = [
            ("Crear Personaje", self.show_create_character),
            ("Mis Personajes", self.show_characters),
            ("Crear Partida", self.show_create_session),
            ("Unirse a Partida", self.show_join_session)
        ]
        
        if current_user and current_user['role'] == 'game_master':
            buttons.append(("Iniciar Combate", self.show_start_combat))
        
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(content_frame, text=text, command=command, width=25)
            btn.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
        
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
    
    def show_create_character(self):
        form_window = tk.Toplevel(self.root)
        form_window.title("Crear Personaje")
        form_window.geometry("400x300")
        
        ttk.Label(form_window, text="Crear Personaje", style="Title.TLabel").pack(pady=10)
        
        form_frame = ttk.Frame(form_window)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        name_entry = ttk.Entry(form_frame)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Raza:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        race_combobox = ttk.Combobox(form_frame, values=["Humano", "Elfo", "Enano", "Orco"])
        race_combobox.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Clase:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        class_combobox = ttk.Combobox(form_frame, values=["Guerrero", "Mago", "Ladrón", "Clérigo"])
        class_combobox.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(form_frame, text="Crear", command=lambda: self.create_character(
            name_entry.get(),
            race_combobox.get(),
            class_combobox.get(),
            form_window
        )).grid(row=3, columnspan=2, pady=10)
    
    def create_character(self, name, race, char_class, window):
        if not all([name, race, char_class]):
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return
        
        result = CharacterDAO.create_character(name, race, char_class)
        if result:
            messagebox.showinfo("Éxito", "Personaje creado exitosamente")
            window.destroy()
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "No se pudo crear el personaje")
    
    def show_characters(self):
        characters = CharacterDAO.get_characters()
        list_window = tk.Toplevel(self.root)
        list_window.title("Mis Personajes")
        list_window.geometry("600x400")
        
        tree = ttk.Treeview(list_window, columns=("ID", "Nombre", "Raza", "Clase"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Raza", text="Raza")
        tree.heading("Clase", text="Clase")
        
        for char in characters:
            tree.insert("", tk.END, values=(char['id'], char['name'], char['race'], char['class']))
        
        tree.pack(fill=tk.BOTH, expand=True)
    
    def show_create_session(self):
        form_window = tk.Toplevel(self.root)
        form_window.title("Crear Partida")
        form_window.geometry("300x150")
        
        ttk.Label(form_window, text="ID Aventura:").pack(pady=5)
        adventure_entry = ttk.Entry(form_window)
        adventure_entry.pack(pady=5)
        
        ttk.Button(form_window, text="Crear", command=lambda: self.create_session(
            adventure_entry.get(),
            form_window
        )).pack(pady=10)
    
    def create_session(self, adventure_id, window):
        if not adventure_id.isdigit():
            messagebox.showwarning("Error", "ID debe ser numérico")
            return
        
        result = GameSessionDAO.create_session(int(adventure_id))
        if result:
            messagebox.showinfo("Éxito", "Partida creada exitosamente")
            window.destroy()
        else:
            messagebox.showerror("Error", "No se pudo crear la partida")
    
    def show_join_session(self):
        form_window = tk.Toplevel(self.root)
        form_window.title("Unirse a Partida")
        form_window.geometry("300x200")
        
        ttk.Label(form_window, text="ID Partida:").pack(pady=5)
        session_entry = ttk.Entry(form_window)
        session_entry.pack(pady=5)
        
        ttk.Label(form_window, text="ID Personaje:").pack(pady=5)
        char_entry = ttk.Entry(form_window)
        char_entry.pack(pady=5)
        
        ttk.Button(form_window, text="Unirse", command=lambda: self.join_session(
            session_entry.get(),
            char_entry.get(),
            form_window
        )).pack(pady=10)
    
    def join_session(self, session_id, char_id, window):
        if not all([session_id.isdigit(), char_id.isdigit()]):
            messagebox.showwarning("Error", "IDs deben ser numéricos")
            return
        
        result = GameSessionDAO.join_session(int(session_id), int(char_id))
        if result:
            messagebox.showinfo("Éxito", "Unido a la partida exitosamente")
            window.destroy()
        else:
            messagebox.showerror("Error", "No se pudo unir a la partida")
    
    def show_start_combat(self):
        form_window = tk.Toplevel(self.root)
        form_window.title("Iniciar Combate")
        form_window.geometry("300x100")
        
        ttk.Label(form_window, text="ID Partida:").pack(pady=5)
        session_entry = ttk.Entry(form_window)
        session_entry.pack(pady=5)
        
        ttk.Button(form_window, text="Iniciar", command=lambda: self.start_combat(
            session_entry.get(),
            form_window
        )).pack(pady=10)
    
    def start_combat(self, session_id, window):
        if not session_id.isdigit():
            messagebox.showwarning("Error", "ID debe ser numérico")
            return
        
        result = CombatDAO.start_combat(int(session_id))
        if result:
            messagebox.showinfo("Éxito", "Combate iniciado exitosamente")
            window.destroy()
        else:
            messagebox.showerror("Error", "No se pudo iniciar el combate")
    
    def logout(self):
        LocalStorage.remove_item('access_token')
        LocalStorage.remove_item('user')
        self.root.destroy()
        show_login_window()

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("RolPlayer - Login")
        self.root.geometry("400x200")
        
        configure_styles()
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Iniciar Sesión", style="Title.TLabel").pack(pady=10)
        
        ttk.Label(main_frame, text="Usuario:").pack(pady=5)
        self.user_entry = ttk.Entry(main_frame)
        self.user_entry.pack(pady=5)
        
        ttk.Label(main_frame, text="Contraseña:").pack(pady=5)
        self.pass_entry = ttk.Entry(main_frame, show="*")
        self.pass_entry.pack(pady=5)
        
        ttk.Button(main_frame, text="Ingresar", command=self.do_login).pack(pady=10)
    
    def do_login(self):
        user = self.user_entry.get()
        password = self.pass_entry.get()
        
        if not user or not password:
            messagebox.showwarning("Error", "Usuario y contraseña requeridos")
            return
        
        result = AuthDAO.login(user, password)
        if result:
            self.root.destroy()
            root = tk.Tk()
            MainApp(root)
            root.mainloop()

def show_login_window():
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    show_login_window()