import requests
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import urllib3
import jwt
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- MODELOS COMPLETOS ---
class Usuari:
    def __init__(self, id, nom_usuari, correu, nom, cognom, rol):
        self.id = id
        self.nom_usuari = nom_usuari
        self.correu = correu
        self.nom = nom
        self.cognom = cognom
        self.rol = rol

    def __str__(self):
        return (f"Usuari: {self.nom} {self.cognom} ({self.rol})\n"
                f"Correu: {self.correu}\nNom d'usuari: {self.nom_usuari}")

class Nen:
    def __init__(self, id, nom, data_naixement, informacio_medica):
        self.id = id
        self.nom = nom
        self.data_naixement = data_naixement
        self.informacio_medica = informacio_medica

    def __str__(self):
        return (f"Nom: {self.nom}\n"
                f"Data naixement: {self.data_naixement}\n"
                f"Informació mèdica: {self.informacio_medica}")

class Tap:
    def __init__(self, id, nen_id, data, hora, estat, hores_totals):
        self.id = id
        self.nen_id = nen_id
        self.data = data
        self.hora = hora
        self.estat = estat
        self.hores_totals = hores_totals

    def __str__(self):
        return (f"Data: {self.data} {self.hora}\n"
                f"Estat: {self.estat}\n"
                f"Hores totals: {self.hores_totals}")

# --- AUTH MANAGER COMPLETO ---
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
                            'nom': decoded.get('nom', ''),
                            'cognom': decoded.get('cognom', ''),
                            'correu': decoded.get('correu', ''),
                            'nom_usuari': decoded.get('nom_usuari', '')
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
            decoded = jwt.decode(self.token, options={"verify_signature": False})
            resposta = requests.get(
                "http://127.0.0.1:5000/perfil",
                headers={'Authorization': f'Bearer {self.token}'},
                timeout=3,
                verify=False
            )
            return resposta.status_code == 200
        except Exception as e:
            print(f"Error validando sesión: {str(e)}")
            return False

# --- DAOs COMPLETOS ---
class DaoUsuari:
    def __init__(self, auth_manager):
        self.base_url = "http://127.0.0.1:5000"
        self.auth_manager = auth_manager
    
    def iniciar_sessio(self, correu, contrasenya):
        try:
            resposta = requests.post(
                f"{self.base_url}/login",  # Cambiar a /login
                json={"username": correu, "password": contrasenya},  # Ajustar parámetros
                headers={'Content-Type': 'application/json'},
                timeout=10,
                verify=False
            )

            if resposta.status_code == 200:
                dades = resposta.json()
                if dades.get("coderesponse") == "1":
                    self.auth_manager.guardar_sessio(
                        dades['token'],
                        dades['username'],
                        dades['idrole']
                    )
                    return Usuari(
                        dades['id'],
                        dades['username'],
                        dades['email'],
                        "",  # Nombre no proporcionado
                        "",  # Apellido no proporcionado
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
                f"{self.base_url}/child",  # Cambiar a /child
                json={"iduser": self.auth_manager.usuari['id']},  # Enviar iduser
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
                        "",  # Data de nacimiento no proporcionada
                        ""   # Información médica no proporcionada
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
                f"{self.base_url}/taps",  # Cambiar a /taps
                json={"idchild": idchild, "data": data},  # Ajustar parámetros
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
                        t['init'].split("T")[0],
                        t['init'].split("T")[1],
                        t['status_id'],
                        t.get('end', None)
                    ) for t in dades.get("data", [])]
                else:
                    return f"Error: {dades.get('msg', 'Error desconocido')}"
            return f"Error: {resposta.json().get('msg', 'Error desconegut')}"
        except requests.exceptions.RequestException as e:
            return f"Error de connexió: {str(e)}"

# --- INTERFAZ TKINTER COMPLETA ---
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
            self._actualizar_datos_usuario_desde_token()
            self._mostrar_menu_principal()
        else:
            self._mostrar_login()

    def _crear_interfaz(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self._crear_pantalla_login()
        self._crear_pantalla_menu()
        self._crear_pantalla_perfil()
        self._crear_pantalla_nens()
        self._crear_pantalla_taps()
        self._crear_pantalla_crear_usuari()
        self._crear_pantalla_crear_nen()
        self._crear_pantalla_crear_tap()

    def _crear_pantalla_login(self):
        self.frame_login = ttk.Frame(self.main_frame)
        
        ttk.Label(self.frame_login, text="Inici de Sessió", style='Header.TLabel').pack(pady=20)
        
        frame_form = ttk.Frame(self.frame_login)
        frame_form.pack(pady=20)
        
        ttk.Label(frame_form, text="Correu electrònic:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_correu = ttk.Entry(frame_form, width=30)
        self.entry_correu.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_form, text="Contrasenya:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_contrasenya = ttk.Entry(frame_form, width=30, show="*")
        self.entry_contrasenya.grid(row=1, column=1, padx=5, pady=5)
        
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
        ttk.Button(btn_frame, text="Afegir Usuari", command=lambda: self._mostrar_crear('usuari'), width=20).pack(pady=10)
        ttk.Button(btn_frame, text="Afegir Nen", command=lambda: self._mostrar_crear('nen'), width=20).pack(pady=10)
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
        
        columns = ('nom', 'data_naixement', 'informacio_medica')
        self.tree_nens = ttk.Treeview(self.frame_nens, columns=columns, show='headings', height=15)
        
        self.tree_nens.heading('nom', text='Nom')
        self.tree_nens.heading('data_naixement', text='Data Naixement')
        self.tree_nens.heading('informacio_medica', text='Informació Mèdica')
        
        self.tree_nens.column('nom', width=200)
        self.tree_nens.column('data_naixement', width=150)
        self.tree_nens.column('informacio_medica', width=400)
        
        scrollbar = ttk.Scrollbar(self.frame_nens, orient=tk.VERTICAL, command=self.tree_nens.yview)
        self.tree_nens.configure(yscroll=scrollbar.set)
        
        self.tree_nens.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Button(self.frame_nens, text="Tornar al Menú", command=self._mostrar_menu_principal).pack(pady=10)

    def _crear_pantalla_taps(self):
        self.frame_taps = ttk.Frame(self.main_frame)
        
        ttk.Label(self.frame_taps, text="Taps dels Nens", style='Header.TLabel').pack(pady=10)
        
        columns = ('data', 'hora', 'estat', 'hores_totals')
        self.tree_taps = ttk.Treeview(self.frame_taps, columns=columns, show='headings', height=15)
        
        self.tree_taps.heading('data', text='Data')
        self.tree_taps.heading('hora', text='Hora')
        self.tree_taps.heading('estat', text='Estat')
        self.tree_taps.heading('hores_totals', text='Hores Totals')
        
        self.tree_taps.column('data', width=120)
        self.tree_taps.column('hora', width=80)
        self.tree_taps.column('estat', width=100)
        self.tree_taps.column('hores_totals', width=100)
        
        scrollbar = ttk.Scrollbar(self.frame_taps, orient=tk.VERTICAL, command=self.tree_taps.yview)
        self.tree_taps.configure(yscroll=scrollbar.set)
        
        self.tree_taps.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Button(self.frame_taps, text="Tornar al Menú", command=self._mostrar_menu_principal).pack(pady=10)

    def _crear_pantalla_crear_usuari(self):
        self.frame_crear_usuari = ttk.Frame(self.main_frame)
        
        ttk.Label(self.frame_crear_usuari, text="Crear Nou Usuari", style='Header.TLabel').pack(pady=10)
        
        frame_form = ttk.Frame(self.frame_crear_usuari)
        frame_form.pack(pady=10)
        
        campos = [
            ("Nom d'usuari:", "entry_nom_usuari"),
            ("Contrasenya:", "entry_contrasenya_usuari", True),
            ("Correu:", "entry_correu_usuari"),
            ("Nom:", "entry_nom_usuari"),
            ("Cognom:", "entry_cognom_usuari"),
            ("Rol (tutor/cuidador):", "entry_rol_usuari")
        ]
        
        for i, (texto, attr, *opciones) in enumerate(campos):
            ttk.Label(frame_form, text=texto).grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
            entry = ttk.Entry(frame_form, width=30, show="*" if opciones and opciones[0] else None)
            entry.grid(row=i, column=1, padx=5, pady=5)
            setattr(self, attr, entry)
        
        btn_frame = ttk.Frame(self.frame_crear_usuari)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Crear Usuari", command=self._crear_usuari).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel·lar", command=self._mostrar_menu_principal).pack(side=tk.LEFT, padx=5)

    def _crear_pantalla_crear_nen(self):
        self.frame_crear_nen = ttk.Frame(self.main_frame)
        
        ttk.Label(self.frame_crear_nen, text="Afegir Nou Nen", style='Header.TLabel').pack(pady=10)
        
        frame_form = ttk.Frame(self.frame_crear_nen)
        frame_form.pack(pady=10)
        
        campos = [
            ("Nom:", "entry_nom_nen"),
            ("Data Naixement (YYYY-MM-DD):", "entry_data_naixement"),
            ("Informació Mèdica:", "entry_info_medica"),
            ("ID Tutor:", "entry_tutor_id"),
            ("ID Cuidador:", "entry_cuidador_id")
        ]
        
        for i, (texto, attr) in enumerate(campos):
            ttk.Label(frame_form, text=texto).grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
            entry = ttk.Entry(frame_form, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            setattr(self, attr, entry)
        
        btn_frame = ttk.Frame(self.frame_crear_nen)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Afegir Nen", command=self._crear_nen).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel·lar", command=self._mostrar_menu_principal).pack(side=tk.LEFT, padx=5)

    def _crear_pantalla_crear_tap(self):
        self.frame_crear_tap = ttk.Frame(self.main_frame)
        
        ttk.Label(self.frame_crear_tap, text="Registrar Nou Tap", style='Header.TLabel').pack(pady=10)
        
        frame_form = ttk.Frame(self.frame_crear_tap)
        frame_form.pack(pady=10)
        
        campos = [
            ("ID Nen:", "entry_nen_id"),
            ("Data (YYYY-MM-DD):", "entry_data_tap"),
            ("Hora (HH:MM:SS):", "entry_hora_tap"),
            ("Estat:", "entry_estat_tap"),
            ("Hores Totals:", "entry_hores_totals")
        ]
        
        for i, (texto, attr) in enumerate(campos):
            ttk.Label(frame_form, text=texto).grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
            entry = ttk.Entry(frame_form, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            setattr(self, attr, entry)
        
        btn_frame = ttk.Frame(self.frame_crear_tap)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Registrar Tap", command=self._crear_tap).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel·lar", command=self._mostrar_menu_principal).pack(side=tk.LEFT, padx=5)

    def _actualizar_datos_usuario_desde_token(self):
        try:
            decoded = jwt.decode(
                self.auth_manager.token,
                options={"verify_signature": False}
            )
            if 'user_id' in decoded:
                if not self.auth_manager.usuari.get('nom'):
                    self.auth_manager.usuari.update({
                        'nom': decoded.get('nom', ''),
                        'cognom': decoded.get('cognom', ''),
                        'correu': decoded.get('correu', ''),
                        'nom_usuari': decoded.get('nom_usuari', '')
                    })
        except Exception as e:
            print(f"Error actualizando datos: {str(e)}")

    def _mostrar_login(self):
        self._amagar_todas_pantallas()
        self.frame_login.pack(fill=tk.BOTH, expand=True)
        self.entry_correu.focus()

    def _mostrar_menu_principal(self):
        self._amagar_todas_pantallas()
        self.lbl_titol_menu.config(
            text=f"Benvingut/da {self.auth_manager.usuari['nom']} ({self.auth_manager.rol})"
        )
        self.frame_menu.pack(fill=tk.BOTH, expand=True)

    def _mostrar_perfil(self):
        self._amagar_todas_pantallas()
        usuari = f"Nom: {self.auth_manager.usuari['nom']} {self.auth_manager.usuari['cognom']}\n"
        usuari += f"Rol: {self.auth_manager.rol}\n"
        usuari += f"Correu: {self.auth_manager.usuari['correu']}\n"
        usuari += f"Nom d'usuari: {self.auth_manager.usuari['nom_usuari']}"
        
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
                    nen.nom,
                    nen.data_naixement,
                    nen.informacio_medica
                ))
        else:
            messagebox.showerror("Error", resultat)
        
        self.frame_nens.pack(fill=tk.BOTH, expand=True)

    def _mostrar_taps(self):
        self._amagar_todas_pantallas()
        
        for item in self.tree_taps.get_children():
            self.tree_taps.delete(item)
        
        resultat = self.dao_tap.obtenir_taps()
        
        if isinstance(resultat, list):
            for tap in resultat:
                self.tree_taps.insert('', tk.END, values=(
                    tap.data,
                    tap.hora,
                    tap.estat,
                    tap.hores_totals
                ))
        else:
            messagebox.showerror("Error", resultat)
        
        self.frame_taps.pack(fill=tk.BOTH, expand=True)

    def _mostrar_crear(self, tipo):
        self._amagar_todas_pantallas()
        if tipo == 'usuari':
            self.frame_crear_usuari.pack(fill=tk.BOTH, expand=True)
        elif tipo == 'nen':
            self.frame_crear_nen.pack(fill=tk.BOTH, expand=True)
        elif tipo == 'tap':
            self.frame_crear_tap.pack(fill=tk.BOTH, expand=True)

    def _amagar_todas_pantallas(self):
        for frame in (
            self.frame_login, 
            self.frame_menu, 
            self.frame_perfil, 
            self.frame_nens, 
            self.frame_taps,
            self.frame_crear_usuari,
            self.frame_crear_nen,
            self.frame_crear_tap
        ):
            frame.pack_forget()

    def _iniciar_sessio(self):
        correu = self.entry_correu.get()
        contrasenya = self.entry_contrasenya.get()
        
        if not correu or not contrasenya:
            messagebox.showerror("Error", "Si us plau, introdueix correu i contrasenya")
            return
        
        resultat = self.dao_usuari.iniciar_sessio(correu, contrasenya)
        
        if isinstance(resultat, Usuari):
            self.auth_manager.usuari = {
                'id': resultat.id,
                'nom': resultat.nom,
                'cognom': resultat.cognom,
                'correu': resultat.correu,
                'nom_usuari': resultat.nom_usuari
            }
            self._mostrar_menu_principal()
        else:
            messagebox.showerror("Error", resultat)

    def _tancar_sessio(self):
        self.auth_manager.tancar_sessio()
        self.entry_correu.delete(0, tk.END)
        self.entry_contrasenya.delete(0, tk.END)
        self._mostrar_login()

    def _crear_usuari(self):
        try:
            nou_usuari = {
                "nom_usuari": self.entry_nom_usuari.get(),
                "contrasenya": self.entry_contrasenya_usuari.get(),
                "correu": self.entry_correu_usuari.get(),
                "nom": self.entry_nom_usuari.get(),
                "cognom": self.entry_cognom_usuari.get(),
                "rol": self.entry_rol_usuari.get()
            }
            
            resposta = requests.post(
                "http://127.0.0.1:5000/crear_usuari",
                json=nou_usuari,
                headers={'Content-Type': 'application/json'},
                verify=False
            )
            
            if resposta.status_code == 201:
                messagebox.showinfo("Èxit", "Usuari creat correctament")
                self._mostrar_menu_principal()
            else:
                messagebox.showerror("Error", resposta.json().get('error', 'Error desconegut'))
        except Exception as e:
            messagebox.showerror("Error", f"No s'ha pogut crear l'usuari: {str(e)}")

    def _crear_nen(self):
        try:
            nou_nen = {
                "tutor_id": int(self.entry_tutor_id.get()),
                "cuidador_id": int(self.entry_cuidador_id.get()),
                "nom": self.entry_nom_nen.get(),
                "data_naixement": self.entry_data_naixement.get(),
                "informacio_medica": self.entry_info_medica.get()
            }
            
            resposta = requests.post(
                "http://127.0.0.1:5000/crear_nen",
                json=nou_nen,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.auth_manager.token}'
                },
                verify=False
            )
            
            if resposta.status_code == 201:
                messagebox.showinfo("Èxit", "Nen afegit correctament")
                self._mostrar_menu_principal()
            else:
                messagebox.showerror("Error", resposta.json().get('error', 'Error desconegut'))
        except Exception as e:
            messagebox.showerror("Error", f"No s'ha pogut afegir el nen: {str(e)}")

    def _crear_tap(self):
        try:
            nou_tap = {
                "nen_id": int(self.entry_nen_id.get()),
                "data": self.entry_data_tap.get(),
                "hora": self.entry_hora_tap.get(),
                "estat": self.entry_estat_tap.get(),
                "hores_totals": float(self.entry_hores_totals.get())
            }
            
            resposta = requests.post(
                "http://127.0.0.1:5000/crear_tap",
                json=nou_tap,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.auth_manager.token}'
                },
                verify=False
            )
            
            if resposta.status_code == 201:
                messagebox.showinfo("Èxit", "Tap registrat correctament")
                self._mostrar_menu_principal()
            else:
                messagebox.showerror("Error", resposta.json().get('error', 'Error desconegut'))
        except Exception as e:
            messagebox.showerror("Error", f"No s'ha pogut registrar el tap: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacio(root)
    root.mainloop()
