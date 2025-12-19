from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox
from database.db_manager import db
import database.supabase_db_manager as supabase_db

# Configuración global de apariencia
ctk.set_appearance_mode("dark")     # "light", "dark" o "system"
ctk.set_default_color_theme("blue") # puedes usar "dark-blue", "green", etc. // Se puede implementar más adelante una pestaña de configuración del sistema.

DB_PATH = Path("./database/TFG_database.db")

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_login_success, on_register, **kwargs):
        super().__init__(master, **kwargs)
        self.on_login_success = on_login_success
        self.on_register = on_register

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=0)
        self.grid_rowconfigure(7, weight=1)

        title = ctk.CTkLabel(
            self,
            text="Iniciar sesión",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, pady=(40, 20), padx=40, sticky="n")

        self.username_entry = ctk.CTkEntry(
            self,
            placeholder_text="Usuario",
            width=260
        )
        self.username_entry.grid(row=1, column=0, pady=10, padx=40)

        self.password_entry = ctk.CTkEntry(
            self,
            placeholder_text="Contraseña",
            show="*",
            width=260
        )
        self.password_entry.grid(row=2, column=0, pady=10, padx=40)

        login_button = ctk.CTkButton(
            self,
            text="Entrar",
            width=260,
            command=lambda: self._handle_login()
        )
        login_button.grid(row=3, column=0, pady=(20, 10), padx=40)

        info_label = ctk.CTkLabel(
            self,
            text="Introduce tus credenciales para continuar.",
            font=ctk.CTkFont(size=12)
        )
        info_label.grid(row=4, column=0, pady=(0, 20), padx=40)

        register_button = ctk.CTkButton(
            self,
            text="Registrarse",
            width=260,
            command=lambda: self._new_user_register()
        )
        register_button.grid(row=5, column=0, pady=(20, 10), padx=40)

   

    def _handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        print(f"[DEBUG] Intentando login con username='{username}' y password='{password}'")

        # Aquí deberías sustituir esta validación básica por tu lógica real
        if not username or not password:
            messagebox.showwarning("Error", "Usuario y contraseña son obligatorios.")
            return

        # Llamar API / base de datos aquí.
        if supabase_db.check_user_credentials(username, password):
            self.on_login_success(username, None)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")

    
    #Se hacen consultas a base de datos con usuarios y contraseñas encriptadas
    def check_credentials_from_sqlite_db(self, username: str, password: str) -> bool:
        #Devuelve True si (username, password) se encuentra en el CSV, False si no.
        if not DB_PATH.exists():
            return False  #Podría lanzar una excepción si no 

        #Verifica que el username y el password concuerden         
        user = db.verify_user(username, password)

        if user is not None:
            id_usuario = user["id"]
            user_name = user["username"]
            #print(f"[DEBUG]: {user_name} tiene id: {id_usuario}")
            return True
        return False    

    def _new_user_register(self):
        if self.on_register:
            self.on_register()

   
        
        


        
