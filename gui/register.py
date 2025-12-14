import sqlite3
from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox
import csv
from database.db_manager import db

# Configuración global de apariencia
ctk.set_appearance_mode("dark")     # "light", "dark" o "system"
ctk.set_default_color_theme("blue") # puedes usar "dark-blue", "green", etc. // Se puede implementar más adelante una pestaña de configuración del sistema.

DB_PATH = Path("./database/users.csv")

class RegisterFrame(ctk.CTkFrame):
    def __init__(self, master, on_register_success, **kwargs):
        super().__init__(master, **kwargs)
        self.on_register_success = on_register_success

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=0)
        self.grid_rowconfigure(5, weight=1)
        
        title = ctk.CTkLabel(
            self,
            text="Panel de Registro",
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
            text="Registrarse",
            width=260,
            command=self._handle_register
        )
        login_button.grid(row=3, column=0, pady=(20, 10), padx=40)

        info_label = ctk.CTkLabel(
            self,
            text="Introduce tus credenciales para continuar.",
            font=ctk.CTkFont(size=12)
        )
        info_label.grid(row=4, column=0, pady=(0, 20), padx=40)


    def _handle_register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        #print(f"[DEBUG] Intentando registrar con username='{username}' y password='{password}'")
        self.add_user_toDB(username, password)
        self.on_register_success()  

        # Llamar API / base de datos aquí.


    #Versión anticuada, ya no se registran usuarios en un csv, se registran usuarios en una basde de datos, usar add_user_toDB mejor
    def add_user_toCSV(self, username: str, password: str):
        file_exists = DB_PATH.exists()

        # AQUÍ: abrimos el Path, no usamos DictWriter sobre DB_PATH directamente
        with DB_PATH.open("a", newline="", encoding="utf-8") as f:
            fieldnames = ["username", "password"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)  # DictWriter(f), no DB_PATH

            if not file_exists:
                writer.writeheader()

            writer.writerow({
                "username": username,
                "password": password,
            })
        

    def add_user_toDB(self, username: str, password: str):
            #Crea el usuario en la base de datos de sqlite
            if db.create_user(username=username, password= password, email= None) == False:            
                messagebox.showwarning(title="Ya existe un usuario con ese nombre", 
                                       message="Pruebe con otro nombre de usuario. \n \n" \
                                       "Abortando registro de usuario.", icon="warning")
            else:
                 messagebox.showwarning(title="Felicidades!", message= "Usuario creado con éxito", icon="info")


    






        
