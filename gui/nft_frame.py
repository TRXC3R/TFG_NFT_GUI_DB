# pip install customtkinter
import os 
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import api.sd_api as sd_api


# Configuración global de apariencia
ctk.set_appearance_mode("dark")     # "light", "dark" o "system"
ctk.set_default_color_theme("blue") # puedes usar "dark-blue", "green", etc.


class NFTFrame(ctk.CTkFrame):
    def __init__(self, master, username, img, on_generate_callback=None, on_click_menu= None, on_imagen_generada = None, **kwargs):
        super().__init__(master, **kwargs)
        self.username = username
        self.on_generate_callback = on_generate_callback
        self.on_click_menu = on_click_menu
        self.on_imagen_generada = on_imagen_generada
        self.img = img

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        #Verificar que el usuario tiene su carpeta de imágenes
        user_image_dir = f'./output_images/{self.username}'
        if not os.path.exists(user_image_dir):
            os.makedirs(user_image_dir)
            print(f"[DEBUG] Creada carpeta de imágenes para el usuario '{self.username}' en '{user_image_dir}'")
        else:
            print(f"[DEBUG] Carpeta de imágenes para el usuario '{self.username}' ya existe en '{user_image_dir}'") 
            

        # Cabecera
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=0)

        title = ctk.CTkLabel(
            header_frame,
            text="Crear NFT",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w")

        user_label = ctk.CTkLabel(
            header_frame,
            text=f"Conectado como: {self.username}",
            font=ctk.CTkFont(size=12)
        )
        user_label.grid(row=0, column=1, sticky="e")

        menu_button = ctk.CTkButton(
            header_frame,
            text="Menú",
            width=80,
            command= self.show_menu
        )
        menu_button.grid(row=0, column=2, sticky="e", padx=(10,0))

        # Zona izquierda: 
        # formulario (prompt + estilo + steps + botón)

        form_frame = ctk.CTkFrame(self, corner_radius=12)
        form_frame.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=(10, 20))
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_rowconfigure(1, weight=1)

        prompt_label = ctk.CTkLabel(
            form_frame,
            text="Prompt para la imagen del NFT:",
            font=ctk.CTkFont(size=14, weight="bold") 
        )
        prompt_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 5)) #Que sea grande 

        self.prompt_text = ctk.CTkTextbox(
            form_frame,
            height=160
        )
        self.prompt_text.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))

        style_label = ctk.CTkLabel(
            form_frame,
            text="Estilo de la imagen:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        style_label.grid(row=2, column=0, sticky="w", padx=20, pady=(10, 5))

        self.style_combobox = ctk.CTkComboBox(
            form_frame,
            values=["Realista", "Anime", "Pixel Art", "Cyberpunk", "Low Poly", "Ilustración 2D"],
            state="readonly"
        )
        self.style_combobox.set("Anime")  # valor por defecto
        self.style_combobox.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))

        steps_label = ctk.CTkLabel(
            form_frame,
            text="Número de pasos de generación:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        steps_label.grid(row=4, column=0, sticky="w", padx=20, pady=(10, 5))   
        
        self.steps_spinbox = ctk.CTkComboBox(
            form_frame,
            values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
            state="readonly"
        )
        self.steps_spinbox.set("5")  # valor por defecto
        self.steps_spinbox.grid(row=5, column=0, sticky="ew", padx=20, pady=(0, 20))


        generate_button = ctk.CTkButton(
            form_frame,
            text="Generar imagen",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.recopilar_y_generar

        )
        generate_button.grid(row=6, column=0, sticky="ew", padx=20, pady=(0, 20))

        # Zona derecha: previsualización (placeholder)
        preview_frame = ctk.CTkFrame(self, corner_radius=12)
        preview_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=(10, 20))
        preview_frame.grid_rowconfigure(1, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)

        preview_label = ctk.CTkLabel(
            preview_frame,
            text="Previsualización",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        preview_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 5))

        if not img:
            print("No hay imagen aún, escribe un prompt")
            self.image_placeholder = ctk.CTkLabel(
                preview_frame,
                text="Aquí se mostrará la imagen generada",
                width=260,
                height=260,
                fg_color="#222222",
                corner_radius=12,
                anchor="center", 
            )
            self.image_placeholder.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))
        else:

            # Cargar la imagen generada 
            # Se puede cambiar la imagen del imagelabel de la siguiente manera: self.image_label.configure(image=self.nft_image)
            ruta_imagen = Image.open(img)
            my_image = ctk.CTkImage(
                light_image=ruta_imagen,
                dark_image=ruta_imagen,
                size=(260, 260)   # ancho, alto en píxeles
            )
            print("Colocando imagen en placeholder")
            self.image_placeholder = ctk.CTkLabel(
                preview_frame,
                text = "",
                image=my_image 
            )
            self.image_placeholder.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))


    # Recopilar datos introducidos en el panel y generar imagen
    def recopilar_y_generar(self):
        prompt = self.prompt_text.get("1.0", "end").strip()
        style = self.style_combobox.get()
        steps = int(self.steps_spinbox.get())
        
        if not prompt:
            messagebox.showwarning("Prompt vacío", "Por favor, escribe un prompt para el NFT.")
            print("[DEBUG] Prompt vacío, no se genera imagen.")
        else:
            #   - Llamar a tu API de IA
            #   - Guardar imagen, mintear NFT, etc.

            #Enseñar por consola para verificar que se recogen bien los datos
            print(f"[DEBUG] Generando NFT con estilo='{style}' y prompt='{prompt[:60]}...'")

            # Mostrar mensaje de generación, hay que presionar ok para continuar
            messagebox.showinfo(
            "Generando NFT",
            f"Generando imagen con estilo '{style}' a partir del prompt:\n\n{prompt[:150]}..."
            )

            # Llamar a la función de generación de imagen
            #imagen_generada = generate_image(prompt, style, steps, username=self.username)
            #imagen_generada = start_generation_thread(prompt, style, steps, username=self.username)
            imagen_generada = sd_api.generate_image(self.username, prompt, style, steps, 0)
            #Una vez generada la imagen Actualizar previsualización
            self.actualizar_previsualizacion(imagen_generada)
        
    def show_menu(self):
        if self.on_click_menu:
            self.on_click_menu(self.username)

    def actualizar_previsualizacion(self, imagen_generada):
        if self.on_imagen_generada:
            self.on_imagen_generada(self.username, imagen_generada)
        

