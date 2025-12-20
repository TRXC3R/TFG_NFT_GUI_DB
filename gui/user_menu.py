import customtkinter as ctk
import os 
import webbrowser

class MenuFrame(ctk.CTkFrame):
    def __init__(self, master, user_id, on_back=None, on_restore_image = None, on_cerrar_sesion = None, **kwargs):
        super().__init__(master, **kwargs)
        self.user_id = user_id
        self.on_back= on_back
        self.on_restore_image = on_restore_image
        self.on_cerrar_sesion = on_cerrar_sesion

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        # Cabecera
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.rowconfigure(1, weight=0)

        back_button = ctk.CTkButton(
            header_frame,
            text="< Volver",
            width=80,
            command= self.go_back_to_nft_page
        )
        back_button.grid(row=0, column=0, sticky="w")

        back_button = ctk.CTkButton(
            header_frame,
            text="Ver Galería de la Comunidad",
            width=80,
            command= lambda: self._open_gallery()
        )
        back_button.grid(row=0, column=2, sticky="w")

        
        text_label = ctk.CTkLabel(
            header_frame,
            text=f"{self.user_id}",
            font=ctk.CTkFont(size=20)
        )
        text_label.grid(row=0, column=3, sticky="e")

        session_close_button = ctk.CTkButton(
            header_frame,
            text="Cerrar Sesión",
            width=80,
            command= self.cerrar_sesion
        )
        session_close_button.grid(row=1, column=3, sticky="w")

        #Listado de imagenes que contiene la carpeta del usuario 
        images_frame = ctk.CTkFrame(self, corner_radius=12)
        images_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=(10, 20))
        images_frame.grid_columnconfigure(0, weight=1)
        images_frame.grid_rowconfigure(0, weight=1)

        images_label = ctk.CTkLabel(
            images_frame,
            text="Tus imágenes generadas:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        images_label.grid(row=0, column=0, sticky="w", padx=20, pady=(10, 5))


        # Lógica para listar las imágenes del usuario
        user_image_dir = f'./output_images/{self.user_id}'
        if os.path.exists(user_image_dir):
            image_files = os.listdir(user_image_dir)
        else:
            image_files = []
        if image_files:
            for idx, image_file in enumerate(image_files):

                #Listar las imagenes en el directorio de cada persona
                image_label = ctk.CTkLabel(
                    images_frame,
                    text=f"{idx + 1}. {image_file}",
                    font=ctk.CTkFont(size=14)
                )
                image_label.grid(row=idx + 1, column=0, sticky="w", padx=40, pady=2)

                #Asignar un boton para recuperar la imagen 
                restore_image_button = ctk.CTkButton(
                    images_frame, text="Restaurar imagen",
                    width=80,
                    command= lambda f = image_file: self.restore_image(f) #Tengo que conjelar el elemento que quiero mostrar "image_file" en cada iteración usando un argumento por defecto en lambda
                )
                restore_image_button.grid(row=idx + 1, column=1, sticky="w")

        else:
            no_images_label = ctk.CTkLabel(
                images_frame,
                text="No has generado ninguna imagen aún.",
                font=ctk.CTkFont(size=14, slant="italic")
            )
            no_images_label.grid(row=1, column=0, sticky="w", padx=40, pady=10)
    
    def go_back_to_nft_page(self):
        if self.on_back:
            self.on_back(self.user_id, img = None)

    def restore_image(self, image_path):
        file = f"./output_images/{self.user_id}/{image_path}"
        print(f"Se quiere recuperar la imagen {file}")
        if self.on_restore_image:
            self.on_restore_image(self.user_id, img = file)

    def mostrar_ruta_imagen(self, path): #No se usa
        print(path)

    def cerrar_sesion(self):
        if self.on_cerrar_sesion:
            self.on_cerrar_sesion()

    def _open_gallery(self):
        # URL donde corre la web con la galeria
        url = "http://127.0.0.1:8000/gallery"
        webbrowser.open(url)