import requests
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import urllib3
import jwt
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- MODELOS ---
class Usuari:
    def __init__(self, id, nom_usuari, correu, token, idrole):
        self.id = id
        self.nom_usuari = nom_usuari
        self.correu = correu
        self.token = token
        self.idrole = idrole

class Nen:
    def __init__(self, id, child_name, sleep_average=None, treatment_id=None, time=None):
        self.id = id
        self.nom = child_name
        self.sleep_average = sleep_average
        self.treatment_id = treatment_id
        self.time = time

class Tap:
    def __init__(self, id, child_id, status_id, user_id, init, end=None):
        self.id = id
        self.child_id = child_id
        self.status_id = status_id
        self.user_id = user_id
        self.init = init
        self.end = end

# --- AUTH MANAGER ---
class AuthManager:
    def __init__(self):
        self.token_file = 'auth_session.json'
        self.token = None
        self.usuari = None
        self.rol = None
        self.carregar_sessio()
    
    def carregar_sessio(self):
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, 'r') as f:
                    data = json.load(f)
                    self.token = data.get('token')
                    if self.token:
                        decoded = jwt.decode(self.token, options={"verify_signature": False})
                        self.usuari = {
                            'id': decoded['user_id'],
                            'nom_usuari': decoded['username'],
                            'rol': decoded['rol']
                        }
                        self.rol = decoded['rol']
            except Exception as e:
                print(f"Error cargando sesión: {str(e)}")
    
    def guardar_sessio(self, token, usuari, rol):
        self.token = token
        self.usuari = usuari
        self.rol = rol
        try:
            with open(self.token_file, 'w') as f:
                json.dump({
                    'token': token,
                    'usuari': usuari,
                    'rol': rol
                }, f)
        except Exception as e:
            print(f"Error guardando sesión: {str(e)}")
    
    def tancar_sessio(self):
        try:
            if os.path.exists(self.token_file):
                os.remove(self.token_file)
        except Exception as e:
            print(f"Error cerrando sesión: {str(e)}")
        self.token = None
        self.usuari = None
        self.rol = None
    
    def sessio_valida(self):
        if not self.token:
            return False
        
        try:
            resposta = requests.post(
                "http://127.0.0.1:5000/login",
                headers={'Authorization': f'Bearer {self.token}'},
                timeout=3,
                verify=False
            )
            return resposta.status_code == 200
        except Exception as e:
            print(f"Error validando sesión: {str(e)}")
            return False

# --- DAOs ---
class DaoUsuari:
    def __init__(self, auth_manager):
        self.base_url = "http://127.0.0.1:5000"
        self.auth_manager = auth_manager
    
    def iniciar_sessio(self, username, password):
        try:
            resposta = requests.post(
                f"{self.base_url}/login",
                json={"username": username, "password": password},
                headers={'Content-Type': 'application/json'},
                timeout=10,
                verify=False
            )

            if resposta.status_code == 200:
                dades = resposta.json()
                if dades.get("coderesponse") == "1":
                    self.auth_manager.guardar_sessio(
                        dades['token'],
                        {
                            'id': dades['id'],
                            'nom_usuari': dades['username'],
                            'correu': dades['email'],
                            'rol': dades['idrole']
                        },
                        dades['idrole']
                    )
                    return Usuari(
                        dades['id'],
                        dades['username'],
                        dades['email'],
                        dades['token'],
                        dades['idrole']
                    )
                else:
                    return f"Error: {dades.get('msg', 'Error desconocido')}"
            else:
                return f"Error: {resposta.json().get('msg', 'Error desconocido')}"
        except Exception as e:
            return f"No s'ha pogut connectar al backend: {str(e)}"

class DaoNen:
    def __init__(self, auth_manager):
        self.base_url = "http://127.0.0.1:5000"
        self.auth_manager = auth_manager

    def obtenir_nens(self):
        try:
            resposta = requests.post(
                f"{self.base_url}/child",
                json={"iduser": self.auth_manager.usuari['id']},
                headers={'Authorization': f'Bearer {self.auth_manager.token}'},
                timeout=5,
                verify=False
            )
            if resposta.status_code == 200:
                dades = resposta.json()
                if dades.get("coderesponse") == "1":
                    return [Nen(
                        n['id'],
                        n['child_name'],
                        n.get('sleep_average'),
                        n.get('treatment_id'),
                        n.get('time')
                    ) for n in dades.get("data", [])]
                else:
                    return f"Error: {dades.get('msg', 'Error desconocido')}"
            return f"Error: {resposta.json().get('msg', 'Error desconegut')}"
        except requests.exceptions.RequestException as e:
            return f"Error de connexió: {str(e)}"

class DaoTap:
    def __init__(self, auth_manager):
        self.base_url = "http://127.0.0.1:5000"
        self.auth_manager = auth_manager

    def obtenir_taps(self, idchild, data=None):
        try:
            resposta = requests.post(
                f"{self.base_url}/taps",
                json={"idchild": idchild, "data": data},
                headers={'Authorization': f'Bearer {self.auth_manager.token}'},
                timeout=5,
                verify=False
            )
            if resposta.status_code == 200:
                dades = resposta.json()
                if dades.get("coderesponse") == "1":
                    return [Tap(
                        t['id'],
                        t['child_id'],
                        t['status_id'],
                        t['user_id'],
                        t['init'],
                        t.get('end')
                    ) for t in dades.get("data", [])]
                else:
                    return f"Error: {dades.get('msg', 'Error desconocido')}"
            return f"Error: {resposta.json().get('msg', 'Error desconegut')}"
        except requests.exceptions.RequestException as e:
            return f"Error de connexió: {str(e)}"

# --- INTERFAZ TKINTER ---
class Aplicacio:
    def __init__(self, root):
        self.root = root
        self.root.title("TapatApp - Gestor de Nens")
        self.root.geometry("1000x700")
        
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'))
        
        self.auth_manager = AuthManager()
        self.dao_usuari = DaoUsuari(self.auth_manager)
        self.dao_nen = DaoNen(self.auth_manager)
        self.dao_tap = DaoTap(self.auth_manager)
        
        self._crear_interfaz()
        
        if self.auth_manager.sessio_valida():
            self._mostrar_menu_principal()
        else:
            self._mostrar_login()

    def _crear_interfaz(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Pantallas
        self._crear_pantalla_login()
        self._crear_pantalla_menu()
        self._crear_pantalla_perfil()
        self._crear_pantalla_nens()
        self._crear_pantalla_taps()
        self._crear_pantalla_crear_tap()

    def _crear_pantalla_login(self):
        self.frame_login = ttk.Frame(self.main_frame)
        
        ttk.Label(self.frame_login, text="Inici de Sessió", style='Header.TLabel').pack(pady=20)
        
        frame_form = ttk.Frame(self.frame_login)
        frame_form.pack(pady=20)
        
        ttk.Label(frame_form, text="Nom d'usuari:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_username = ttk.Entry(frame_form, width=30)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_form, text="Contrasenya:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_password = ttk.Entry(frame_form, width=30, show="*")
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)
        
        btn_frame = ttk.Frame(self.frame_login)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Iniciar Sessió", command=self._iniciar_sessio).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Sortir", command=self.root.quit).pack(side=tk.LEFT, padx=5)

    def _crear_pantalla_menu(self):
        self.frame_menu = ttk.Frame(self.main_frame)
        
        self.lbl_titol_menu = ttk.Label(self.frame_menu, style='Header.TLabel')
        self.lbl_titol_menu.pack(pady=30)
        
        btn_frame = ttk.Frame(self.frame_menu)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="El Meu Perfil", command=self._mostrar_perfil, width=20).pack(pady=10)
        ttk.Button(btn_frame, text="Els Meus Nens", command=self._mostrar_nens, width=20).pack(pady=10)
        ttk.Button(btn_frame, text="Taps dels Nens", command=self._mostrar_taps, width=20).pack(pady=10)
        ttk.Button(btn_frame, text="Registrar Tap", command=lambda: self._mostrar_crear('tap'), width=20).pack(pady=10)
        
        ttk.Button(self.frame_menu, text="Tancar Sessió", command=self._tancar_sessio).pack(pady=30)

    def _crear_pantalla_perfil(self):
        self.frame_perfil = ttk.Frame(self.main_frame)
        
        ttk.Label(self.frame_perfil, text="El Meu Perfil", style='Header.TLabel').pack(pady=20)
        
        self.lbl_info_usuari = ttk.Label(self.frame_perfil, text="", justify=tk.LEFT)
        self.lbl_info_usuari.pack(pady=20, padx=20)
        
        ttk.Button(self.frame_perfil, text="Tornar al Menú", command=self._mostrar_menu_principal).pack(pady=10)

    def _crear_pantalla_nens(self):
        self.frame_nens = ttk.Frame(self.main_frame)
        
        ttk.Label(self.frame_nens, text="Els Meus Nens", style='Header.TLabel').pack(pady=10)
        
        columns = ('id', 'nom', 'sleep_average', 'treatment_id', 'time')
        self.tree_nens = ttk.Treeview(self.frame_nens, columns=columns, show='headings', height=15)
        
        self.tree_nens.heading('id', text='ID')
        self.tree_nens.heading('nom', text='Nom')
        self.tree_nens.heading('sleep_average', text='Mitjana Son')
        self.tree_nens.heading('treatment_id', text='ID Tractament')
        self.tree_nens.heading('time', text='Temps')
        
        self.tree_nens.column('id', width=50)
        self.tree_nens.column('nom', width=150)
        self.tree_nens.column('sleep_average', width=100)
        self.tree_nens.column('treatment_id', width=100)
        self.tree_nens.column('time', width=100)
        
        scrollbar = ttk.Scrollbar(self.frame_nens, orient=tk.VERTICAL, command=self.tree_nens.yview)
        self.tree_nens.configure(yscroll=scrollbar.set)
        
        self.tree_nens.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Button(self.frame_nens, text="Tornar al Menú", command=self._mostrar_menu_principal).pack(pady=10)

    def _crear_pantalla_taps(self):
        self.frame_taps = ttk.Frame(self.main_frame)
        
        ttk.Label(self.frame_taps, text="Taps dels Nens", style='Header.TLabel').pack(pady=10)
        
        columns = ('id', 'child_id', 'status_id', 'user_id', 'init', 'end')
        self.tree_taps = ttk.Treeview(self.frame_taps, columns=columns, show='headings', height=15)
        
        self.tree_taps.heading('id', text='ID')
        self.tree_taps.heading('child_id', text='ID Nen')
        self.tree_taps.heading('status_id', text='Estat')
        self.tree_taps.heading('user_id', text='ID Usuari')
        self.tree_taps.heading('init', text='Inici')
        self.tree_taps.heading('end', text='Fi')
        
        self.tree_taps.column('id', width=50)
        self.tree_taps.column('child_id', width=70)
        self.tree_taps.column('status_id', width=70)
        self.tree_taps.column('user_id', width=70)
        self.tree_taps.column('init', width=150)
        self.tree_taps.column('end', width=150)
        
        scrollbar = ttk.Scrollbar(self.frame_taps, orient=tk.VERTICAL, command=self.tree_taps.yview)
        self.tree_taps.configure(yscroll=scrollbar.set)
        
        self.tree_taps.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Button(self.frame_taps, text="Tornar al Menú", command=self._mostrar_menu_principal).pack(pady=10)

    def _crear_pantalla_crear_tap(self):
        self.frame_crear_tap = ttk.Frame(self.main_frame)
        
        ttk.Label(self.frame_crear_tap, text="Registrar Nou Tap", style='Header.TLabel').pack(pady=10)
        
        frame_form = ttk.Frame(self.frame_crear_tap)
        frame_form.pack(pady=10)
        
        campos = [
            ("ID Nen:", "entry_nen_id"),
            ("Estat (1-4):", "entry_status_id"),
            ("Data (YYYY-MM-DD):", "entry_data"),
            ("Hora Inici (HH:MM:SS):", "entry_hora_inici"),
            ("Hora Fi (HH:MM:SS):", "entry_hora_fi")
        ]
        
        for i, (texto, attr) in enumerate(campos):
            ttk.Label(frame_form, text=texto).grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
            entry = ttk.Entry(frame_form, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            setattr(self, attr, entry)
        
        btn_frame = ttk.Frame(self.frame_crear_tap)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Registrar", command=self._crear_tap).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel·lar", command=self._mostrar_menu_principal).pack(side=tk.LEFT, padx=5)

    # Métodos de navegación
    def _mostrar_login(self):
        self._amagar_todas_pantallas()
        self.frame_login.pack(fill=tk.BOTH, expand=True)
        self.entry_username.focus()

    def _mostrar_menu_principal(self):
        self._amagar_todas_pantallas()
        self.lbl_titol_menu.config(
            text=f"Benvingut/da {self.auth_manager.usuari['nom_usuari']} ({self.auth_manager.rol})"
        )
        self.frame_menu.pack(fill=tk.BOTH, expand=True)

    def _mostrar_perfil(self):
        self._amagar_todas_pantallas()
        usuari = f"Nom d'usuari: {self.auth_manager.usuari['nom_usuari']}\n"
        usuari += f"Rol: {self.auth_manager.rol}\n"
        usuari += f"ID: {self.auth_manager.usuari['id']}"
        
        self.lbl_info_usuari.config(text=usuari)
        self.frame_perfil.pack(fill=tk.BOTH, expand=True)

    def _mostrar_nens(self):
        self._amagar_todas_pantallas()
        
        for item in self.tree_nens.get_children():
            self.tree_nens.delete(item)
        
        resultat = self.dao_nen.obtenir_nens()
        
        if isinstance(resultat, list):
            for nen in resultat:
                self.tree_nens.insert('', tk.END, values=(
                    nen.id,
                    nen.nom,
                    nen.sleep_average,
                    nen.treatment_id,
                    nen.time
                ))
        else:
            messagebox.showerror("Error", resultat)
        
        self.frame_nens.pack(fill=tk.BOTH, expand=True)

    def _mostrar_taps(self):
        self._amagar_todas_pantallas()
        
        for item in self.tree_taps.get_children():
            self.tree_taps.delete(item)
        
        # Obtener el primer niño del usuario para mostrar sus taps
        nens = self.dao_nen.obtenir_nens()
        if isinstance(nens, list) and len(nens) > 0:
            resultat = self.dao_tap.obtenir_taps(nens[0].id)
            
            if isinstance(resultat, list):
                for tap in resultat:
                    self.tree_taps.insert('', tk.END, values=(
                        tap.id,
                        tap.child_id,
                        tap.status_id,
                        tap.user_id,
                        tap.init,
                        tap.end
                    ))
            else:
                messagebox.showerror("Error", resultat)
        else:
            messagebox.showinfo("Informació", "No tens nens registrats")
        
        self.frame_taps.pack(fill=tk.BOTH, expand=True)

    def _mostrar_crear(self, tipo):
        self._amagar_todas_pantallas()
        if tipo == 'tap':
            self.frame_crear_tap.pack(fill=tk.BOTH, expand=True)

    def _amagar_todas_pantallas(self):
        for frame in (
            self.frame_login, 
            self.frame_menu, 
            self.frame_perfil, 
            self.frame_nens, 
            self.frame_taps,
            self.frame_crear_tap
        ):
            frame.pack_forget()

    # Métodos de lógica
    def _iniciar_sessio(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Si us plau, introdueix usuari i contrasenya")
            return
        
        resultat = self.dao_usuari.iniciar_sessio(username, password)
        
        if isinstance(resultat, Usuari):
            self._mostrar_menu_principal()
        else:
            messagebox.showerror("Error", resultat)

    def _tancar_sessio(self):
        self.auth_manager.tancar_sessio()
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self._mostrar_login()

    def _crear_tap(self):
        try:
            # Obtener la fecha y hora del formulario
            data = self.entry_data.get()
            hora_inici = self.entry_hora_inici.get()
            hora_fi = self.entry_hora_fi.get()
            
            # Crear objetos datetime para init y end
            init = f"{data}T{hora_inici}"
            end = f"{data}T{hora_fi}" if hora_fi else None
            
            nou_tap = {
                "child_id": int(self.entry_nen_id.get()),
                "status_id": int(self.entry_status_id.get()),
                "user_id": self.auth_manager.usuari['id'],
                "init": init,
                "end": end
            }
            
            resposta = requests.post(
                "http://127.0.0.1:5000/taps",
                json=nou_tap,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.auth_manager.token}'
                },
                verify=False
            )
            
            if resposta.status_code == 200:
                messagebox.showinfo("Èxit", "Tap registrat correctament")
                self._mostrar_menu_principal()
            else:
                messagebox.showerror("Error", resposta.json().get('msg', 'Error desconegut'))
        except Exception as e:
            messagebox.showerror("Error", f"No s'ha pogut registrar el tap: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacio(root)
    root.mainloop()
