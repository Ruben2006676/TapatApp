import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
import json
import requests
from datetime import datetime

# Configuración de estilos
def configure_styles():
    style = ttk.Style()
    style.theme_use('clam')

    style.configure('.', background='#2E2E2E', foreground='white')
    style.configure('TFrame', background='#2E2E2E')
    style.configure('TLabel', background='#2E2E2E', foreground='white', font=('Arial', 10))
    style.configure('TButton', font=('Arial', 10), padding=5, background='#4A4A4A')
    style.configure('TEntry', font=('Arial', 10), fieldbackground='#4A4A4A')
    style.configure('TCombobox', fieldbackground='#4A4A4A')
    style.configure('Treeview', background='#2E2E2E', fieldbackground='#2E2E2E', foreground='white')
    style.map('Treeview', background=[('selected', '#6B6B6B')])
    style.configure('Treeview.Heading', background='#4A4A4A', foreground='white')
    style.configure('TNotebook', background='#2E2E2E')
    style.configure('TNotebook.Tab', padding=[10, 5], background='#4A4A4A', foreground='white')
    style.configure('Header.TLabel', font=('Arial', 12, 'bold'), foreground='#FFD700')
    style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#FFD700')
    style.configure('Stat.TLabel', font=('Arial', 10, 'bold'), foreground='#FF6347')
    style.configure('Success.TLabel', foreground='#7CFC00')
    style.configure('Danger.TLabel', foreground='#FF4500')
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

class API:
    BASE_URL = "http://localhost:5000"

    @staticmethod
    def register(username, password):
        try:
            response = requests.post(
                f"{API.BASE_URL}/register",
                json={"username": username, "password": password, "email": f"{username}@example.com"}  # Añadido email
            )
            return response.json(), response.status_code
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500

    @staticmethod
    def login(username, password):
        try:
            response = requests.post(
                f"{API.BASE_URL}/login",
                json={"username": username, "password": password}
            )
            return response.json(), response.status_code
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500

    @staticmethod
    def create_character(name, race, char_class, background=""):
        token = LocalStorage.get_item('access_token')
        if not token:
            return None

        try:
            response = requests.post(
                f"{API.BASE_URL}/characters",
                json={
                    "name": name,
                    "race": race,
                    "class": char_class,
                    "background": background
                },
                headers={"Authorization": f"Bearer {token}"}
            )
            return response.json(), response.status_code
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_characters():
        token = LocalStorage.get_item('access_token')
        if not token:
            return None

        try:
            response = requests.get(
                f"{API.BASE_URL}/characters",
                headers={"Authorization": f"Bearer {token}"}
            )
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return None

    @staticmethod
    def get_character_detail(character_id):
        token = LocalStorage.get_item('access_token')
        if not token:
            return None

        try:
            response = requests.get(
                f"{API.BASE_URL}/characters/{character_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return None


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RolPlayer")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
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
        
        logo_frame = ttk.Frame(header_frame)
        logo_frame.pack(side=tk.LEFT)
        
        try:
            logo_img = Image.open('logo.png')
            logo_img = logo_img.resize((40, 40), Image.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = ttk.Label(logo_frame, image=logo_photo)
            logo_label.image = logo_photo
            logo_label.pack(side=tk.LEFT, padx=5)
        except:
            pass
        
        ttk.Label(logo_frame, text="RolPlayer", style="Title.TLabel").pack(side=tk.LEFT)
        
        if current_user:
            user_frame = ttk.Frame(header_frame)
            user_frame.pack(side=tk.RIGHT)
            
            ttk.Label(user_frame, 
                     text=f"Bienvenido, {current_user['username']} (Rol: {current_user['role'].title()})",
                     style="Header.TLabel").pack(side=tk.LEFT)
            
            ttk.Button(user_frame, text="Cerrar Sesión", command=self.logout).pack(side=tk.LEFT, padx=5)
        
        # Contenido principal
        content_frame = ttk.Frame(self.main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        notebook = ttk.Notebook(content_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de Personajes
        characters_tab = ttk.Frame(notebook)
        notebook.add(characters_tab, text="Mis Personajes")
        self.setup_characters_tab(characters_tab)
        
        # Pestaña de Partidas
        sessions_tab = ttk.Frame(notebook)
        notebook.add(sessions_tab, text="Partidas")
        self.setup_sessions_tab(sessions_tab)
        
        if current_user and current_user['role'] == 'game_master':
            combat_tab = ttk.Frame(notebook)
            notebook.add(combat_tab, text="Combate")
            self.setup_combat_tab(combat_tab)
    
    def setup_characters_tab(self, tab):
        action_frame = ttk.Frame(tab)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_frame, text="Crear Nuevo Personaje", 
                  command=self.show_create_character).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame, text="Actualizar Lista", 
                  command=lambda: self.load_characters_list(characters_list)).pack(side=tk.LEFT, padx=5)
        
        list_frame = ttk.Frame(tab)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("ID", "Nombre", "Raza", "Clase", "Nivel")
        characters_list = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            characters_list.heading(col, text=col)
            characters_list.column(col, width=100, anchor=tk.CENTER)
        
        characters_list.column("Nombre", width=150)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=characters_list.yview)
        characters_list.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        characters_list.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(list_frame, text="Ver Detalles", 
                  command=lambda: self.show_character_detail(characters_list)).pack(pady=10)
        
        self.load_characters_list(characters_list)
    
    def load_characters_list(self, treeview):
        for item in treeview.get_children():
            treeview.delete(item)
        
        response, status = API.get_characters()
        
        if status == 200:
            for char in response['characters']:
                treeview.insert("", tk.END, values=(
                    char['id'],
                    char['name'],
                    char['race'],
                    char['class'],
                    char['level']
                ))
        else:
            messagebox.showerror("Error", "No se pudieron cargar los personajes")
    
    def show_character_detail(self, treeview):
        selected_item = treeview.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Selecciona un personaje primero")
            return
        
        character_id = treeview.item(selected_item)['values'][0]
        response, status = API.get_character_detail(character_id)
        
        if status != 200:
            messagebox.showerror("Error", "No se pudo obtener la información del personaje")
            return
        
        character = response
        
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Detalles del Personaje: {character['name']}")
        detail_window.geometry("800x600")
        
        notebook = ttk.Notebook(detail_window)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de Información General
        general_tab = ttk.Frame(notebook)
        notebook.add(general_tab, text="Información General")
        
        main_frame = ttk.Frame(general_tab)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Label(scrollable_frame, text=f"Nombre: {character['name']}", 
                 font=('Arial', 14, 'bold')).pack(pady=10, anchor=tk.W)
        
        try:
            race_img = Image.open(f"races/{character['race'].lower()}.png")
            race_img = race_img.resize((150, 150), Image.LANCZOS)
            race_photo = ImageTk.PhotoImage(race_img)
            race_label = ttk.Label(scrollable_frame, image=race_photo)
            race_label.image = race_photo
            race_label.pack(pady=10)
        except:
            pass
        
        info_frame = ttk.Frame(scrollable_frame)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(info_frame, text=f"Raza: {character['race']}", width=20).pack(side=tk.LEFT)
        ttk.Label(info_frame, text=f"Clase: {character['class']}").pack(side=tk.LEFT)
        
        info_frame2 = ttk.Frame(scrollable_frame)
        info_frame2.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(info_frame2, text=f"Nivel: {character['level']}", width=20).pack(side=tk.LEFT)
        ttk.Label(info_frame2, text=f"Experiencia: {character['experience']}").pack(side=tk.LEFT)
        
        health_frame = ttk.Frame(scrollable_frame)
        health_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(health_frame, text="Salud:").pack(side=tk.LEFT)
        
        health_percent = (character['hit_points'] / character['max_hit_points']) * 100
        health_color = '#4CAF50' if health_percent > 50 else '#FFC107' if health_percent > 25 else '#F44336'
        
        health_canvas = tk.Canvas(health_frame, width=200, height=20, bg='#2E2E2E', highlightthickness=0)
        health_canvas.create_rectangle(0, 0, health_percent * 2, 20, fill=health_color, outline='')
        health_canvas.create_text(100, 10, text=f"{character['hit_points']}/{character['max_hit_points']}", 
                                fill='white', font=('Arial', 10))
        health_canvas.pack(side=tk.LEFT, padx=5)
        
        gold_frame = ttk.Frame(scrollable_frame)
        gold_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(gold_frame, text="Oro:").pack(side=tk.LEFT)
        ttk.Label(gold_frame, text=f"{character['gold']} monedas", style="Success.TLabel").pack(side=tk.LEFT)
        
        background_frame = ttk.Frame(scrollable_frame)
        background_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        ttk.Label(background_frame, text="Historia del Personaje:", style="Header.TLabel").pack(anchor=tk.W)
        
        background_text = scrolledtext.ScrolledText(
            background_frame, 
            wrap=tk.WORD, 
            width=60, 
            height=10,
            bg='#4A4A4A',
            fg='white',
            insertbackground='white',
            font=('Arial', 10)
        )
        background_text.insert(tk.END, character['background'] or "Este personaje no tiene una historia definida.")
        background_text.config(state=tk.DISABLED)
        background_text.pack(fill=tk.BOTH, expand=True)
    
    def show_create_character(self):
        form_window = tk.Toplevel(self.root)
        form_window.title("Crear Personaje")
        form_window.geometry("500x400")
        
        try:
            form_window.iconbitmap('icon.ico')
        except:
            pass
        
        ttk.Label(form_window, text="Crear Nuevo Personaje", style="Title.TLabel").pack(pady=10)
        
        notebook = ttk.Notebook(form_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        basic_tab = ttk.Frame(notebook)
        notebook.add(basic_tab, text="Información Básica")
        
        ttk.Label(basic_tab, text="Nombre:").pack(pady=5)
        self.name_entry = ttk.Entry(basic_tab)
        self.name_entry.pack(pady=5, fill=tk.X, padx=20)
        
        ttk.Label(basic_tab, text="Raza:").pack(pady=5)
        self.race_combobox = ttk.Combobox(basic_tab, values=["Humano", "Elfo", "Enano", "Orco", "Mediano"])
        self.race_combobox.pack(pady=5, fill=tk.X, padx=20)
        
        ttk.Label(basic_tab, text="Clase:").pack(pady=5)
        self.class_combobox = ttk.Combobox(basic_tab, values=["Guerrero", "Mago", "Pícaro", "Clérigo", "Bárbaro", "Bardo"])
        self.class_combobox.pack(pady=5, fill=tk.X, padx=20)
        
        background_tab = ttk.Frame(notebook)
        notebook.add(background_tab, text="Historia")
        
        ttk.Label(background_tab, text="Historia del Personaje:").pack(pady=5)
        self.background_text = scrolledtext.ScrolledText(
            background_tab, 
            wrap=tk.WORD, 
            width=40, 
            height=10,
            bg='#4A4A4A',
            fg='white',
            insertbackground='white',
            font=('Arial', 10)
        )
        self.background_text.pack(pady=5, fill=tk.BOTH, expand=True, padx=10)
        
        ttk.Button(form_window, text="Crear Personaje", 
                  command=lambda: self.create_character(
                      self.name_entry.get(),
                      self.race_combobox.get(),
                      self.class_combobox.get(),
                      self.background_text.get("1.0", tk.END),
                      form_window
                  )).pack(pady=10)
    
    def create_character(self, name, race, char_class, background, window):
        if not all([name, race, char_class]):
            messagebox.showwarning("Error", "Nombre, raza y clase son obligatorios")
            return
        
        response, status = API.create_character(name, race, char_class, background.strip())
        
        if status == 201:
            messagebox.showinfo("Éxito", "Personaje creado exitosamente")
            window.destroy()
            self.show_main_menu()
        else:
            error_msg = response.get('error', 'Error desconocido al crear personaje')
            messagebox.showerror("Error", error_msg)
    
    def setup_sessions_tab(self, tab):
        action_frame = ttk.Frame(tab)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_frame, text="Crear Nueva Partida", 
                  command=self.show_create_session).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame, text="Unirse a Partida", 
                  command=self.show_join_session).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(tab, text="Funcionalidad de partidas en desarrollo...").pack(pady=50)
    
    def setup_combat_tab(self, tab):
        action_frame = ttk.Frame(tab)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_frame, text="Iniciar Combate", 
                  command=self.show_start_combat).pack(side=tk.LEFT, padx=5)
        
        combat_frame = ttk.Frame(tab)
        combat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(combat_frame, text="Simulador de Combate", style="Title.TLabel").pack(pady=10)
        
        canvas = tk.Canvas(combat_frame, bg='#2E2E2E', highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        self.draw_combat_example(canvas)
    
    def draw_combat_example(self, canvas):
        canvas.delete("all")
        canvas.create_rectangle(50, 50, 750, 550, outline='#FFD700', width=2)
        
        for i in range(3):
            x = 150 + i * 200
            y = 150
            canvas.create_oval(x-30, y-30, x+30, y+30, fill='#4CAF50', outline='white')
            canvas.create_text(x, y, text=f"A{i+1}", fill='white', font=('Arial', 12, 'bold'))
        
        for i in range(4):
            x = 100 + i * 150
            y = 400
            canvas.create_oval(x-30, y-30, x+30, y+30, fill='#F44336', outline='white')
            canvas.create_text(x, y, text=f"E{i+1}", fill='white', font=('Arial', 12, 'bold'))
        
        canvas.create_rectangle(800, 50, 950, 550, outline='#FFD700', width=2)
        canvas.create_text(875, 30, text="Iniciativa", fill='white', font=('Arial', 10, 'bold'))
        
        initiatives = ["A2 (18)", "E3 (15)", "A1 (12)", "E1 (10)", "E4 (8)", "A3 (5)", "E2 (3)"]
        
        for i, init in enumerate(initiatives):
            y = 100 + i * 60
            canvas.create_text(875, y, text=init, fill='white', font=('Arial', 10))
            
            if i == 0:
                canvas.create_rectangle(810, y-15, 940, y+15, outline='#FFD700', width=2)
    
    def show_create_session(self):
        form_window = tk.Toplevel(self.root)
        form_window.title("Crear Partida")
        form_window.geometry("400x200")
        
        ttk.Label(form_window, text="Crear Nueva Partida", style="Title.TLabel").pack(pady=10)
        
        form_frame = ttk.Frame(form_window)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(form_frame, text="ID de Aventura:").pack(pady=5)
        adventure_entry = ttk.Entry(form_frame)
        adventure_entry.pack(pady=5, fill=tk.X)
        
        ttk.Button(form_frame, text="Crear Partida", 
                  command=lambda: self.create_session(
                      adventure_entry.get(),
                      form_window
                  )).pack(pady=10)
    
    def create_session(self, adventure_id, window):
        if not adventure_id.isdigit():
            messagebox.showwarning("Error", "El ID de aventura debe ser numérico")
            return
        
        messagebox.showinfo("Info", "Funcionalidad en desarrollo")
        window.destroy()
    
    def show_join_session(self):
        form_window = tk.Toplevel(self.root)
        form_window.title("Unirse a Partida")
        form_window.geometry("400x250")
        
        ttk.Label(form_window, text="Unirse a Partida", style="Title.TLabel").pack(pady=10)
        
        form_frame = ttk.Frame(form_window)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(form_frame, text="ID de Partida:").pack(pady=5)
        session_entry = ttk.Entry(form_frame)
        session_entry.pack(pady=5, fill=tk.X)
        
        ttk.Label(form_frame, text="ID de Personaje:").pack(pady=5)
        char_entry = ttk.Entry(form_frame)
        char_entry.pack(pady=5, fill=tk.X)
        
        ttk.Button(form_frame, text="Unirse a Partida", 
                  command=lambda: self.join_session(
                      session_entry.get(),
                      char_entry.get(),
                      form_window
                  )).pack(pady=10)
    
    def join_session(self, session_id, char_id, window):
        if not all([session_id.isdigit(), char_id.isdigit()]):
            messagebox.showwarning("Error", "Los IDs deben ser numéricos")
            return
        
        messagebox.showinfo("Info", "Funcionalidad en desarrollo")
        window.destroy()
    
    def show_start_combat(self):
        form_window = tk.Toplevel(self.root)
        form_window.title("Iniciar Combate")
        form_window.geometry("400x150")
        
        ttk.Label(form_window, text="Iniciar Combate", style="Title.TLabel").pack(pady=10)
        
        form_frame = ttk.Frame(form_window)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(form_frame, text="ID de Partida:").pack(pady=5)
        session_entry = ttk.Entry(form_frame)
        session_entry.pack(pady=5, fill=tk.X)
        
        ttk.Button(form_frame, text="Iniciar Combate", 
                  command=lambda: self.start_combat(
                      session_entry.get(),
                      form_window
                  )).pack(pady=10)
    
    def start_combat(self, session_id, window):
        if not session_id.isdigit():
            messagebox.showwarning("Error", "El ID de partida debe ser numérico")
            return
        
        messagebox.showinfo("Info", "Funcionalidad en desarrollo")
        window.destroy()
    
    def logout(self):
        LocalStorage.remove_item('access_token')
        LocalStorage.remove_item('refresh_token')
        LocalStorage.remove_item('user')
        self.root.destroy()
        show_login_window()

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("RolPlayer - Login")
        self.root.geometry("500x400")
        
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        configure_styles()
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Pestaña de Login
        login_tab = ttk.Frame(notebook)
        notebook.add(login_tab, text="Iniciar Sesión")
        self.setup_login_tab(login_tab)
        
        # Pestaña de Registro
        register_tab = ttk.Frame(notebook)
        notebook.add(register_tab, text="Registrarse")
        self.setup_register_tab(register_tab)
    
    def setup_login_tab(self, tab):
        form_frame = ttk.Frame(tab)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)
        
        ttk.Label(form_frame, text="Usuario:").pack(pady=5)
        self.login_user_entry = ttk.Entry(form_frame)
        self.login_user_entry.pack(pady=5, fill=tk.X)
        
        ttk.Label(form_frame, text="Contraseña:").pack(pady=5)
        self.login_pass_entry = ttk.Entry(form_frame, show="*")
        self.login_pass_entry.pack(pady=5, fill=tk.X)
        
        ttk.Button(form_frame, text="Ingresar", command=self.do_login).pack(pady=20)
        
        self.login_user_entry.focus_set()
        self.login_pass_entry.bind('<Return>', lambda event: self.do_login())
    
    def setup_register_tab(self, tab):
        form_frame = ttk.Frame(tab)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)
        
        ttk.Label(form_frame, text="Usuario:").pack(pady=5)
        self.register_user_entry = ttk.Entry(form_frame)
        self.register_user_entry.pack(pady=5, fill=tk.X)
        
        ttk.Label(form_frame, text="Contraseña:").pack(pady=5)
        self.register_pass_entry = ttk.Entry(form_frame, show="*")
        self.register_pass_entry.pack(pady=5, fill=tk.X)
        
        ttk.Label(form_frame, text="Confirmar Contraseña:").pack(pady=5)
        self.register_confirm_pass_entry = ttk.Entry(form_frame, show="*")
        self.register_confirm_pass_entry.pack(pady=5, fill=tk.X)
        
        ttk.Button(form_frame, text="Registrarse", command=self.do_register).pack(pady=20)
    
    def do_login(self):
        user = self.login_user_entry.get()
        password = self.login_pass_entry.get()
        
        if not user or not password:
            messagebox.showwarning("Error", "Usuario y contraseña requeridos")
            return
        
        response, status = API.login(user, password)
        
        if status == 200:
            LocalStorage.set_item('access_token', response['access_token'])
            LocalStorage.set_item('refresh_token', response['refresh_token'])
            LocalStorage.set_item('user', json.dumps(response['user']))
            self.root.destroy()
            root = tk.Tk()
            MainApp(root)
            root.mainloop()
        else:
            error_msg = response.get('error', 'Error desconocido al iniciar sesión')
            messagebox.showerror("Error", error_msg)
    
    def do_register(self):
        user = self.register_user_entry.get()
        password = self.register_pass_entry.get()
        confirm_password = self.register_confirm_pass_entry.get()
        
        if not user or not password:
            messagebox.showwarning("Error", "Usuario y contraseña requeridos")
            return
            
        if password != confirm_password:
            messagebox.showwarning("Error", "Las contraseñas no coinciden")
            return
        
        response, status = API.register(user, password)
        
        if status == 201:
            messagebox.showinfo("Éxito", "Usuario registrado exitosamente")
            self.register_user_entry.delete(0, tk.END)
            self.register_pass_entry.delete(0, tk.END)
            self.register_confirm_pass_entry.delete(0, tk.END)
        else:
            error_msg = response.get('error', 'Error desconocido al registrar usuario')
            messagebox.showerror("Error", error_msg)

def show_login_window():
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    show_login_window()