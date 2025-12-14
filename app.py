# pip install customtkinter
import customtkinter as ctk
from gui.login import LoginFrame
from gui.nft_frame import NFTFrame  
from gui.user_menu import MenuFrame
from gui.register import RegisterFrame
from database.db_manager import db



class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NFT Generator - Login & NFT Creator")
        self.geometry("900x550")
        self.minsize(820, 500)

        self.current_frame = None

        # Contenedor principal
        self.container = ctk.CTkFrame(self, corner_radius=0)
        self.container.pack(fill="both", expand=True)

        db.init_db()
        self.show_login()

    def clear_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
            self.current_frame = None

    def show_login(self):
        self.clear_frame()
        self.current_frame = LoginFrame(
            master=self.container,
            on_login_success=self.show_nft_page,
            on_register=self.show_register
        )
        self.current_frame.pack(fill="both", expand=True)

    def show_register(self):
        self.clear_frame()
        self.current_frame = RegisterFrame(
            master=self.container,
            on_register_success=self.show_login
        )
        self.current_frame.pack(fill="both", expand=True)

    def show_nft_page(self, username: str, img):
        self.clear_frame()
        self.current_frame = NFTFrame(
            master=self.container,
            username=username,
            img = img,
            on_generate_callback=self.on_generate_nft,
            on_click_menu=self.show_menu_page, 
            on_imagen_generada = self.show_nft_page
        )
        self.current_frame.pack(fill="both", expand=True)

    def show_menu_page(self, username: str):
        self.clear_frame()
        self.current_frame = MenuFrame(
            master=self.container,
            username=username,
            on_back=self.show_nft_page,
            on_restore_image=self.show_nft_page,
            on_cerrar_sesion=self.show_login
        )
        self.current_frame.pack(fill="both", expand=True)

    def on_generate_nft(self, prompt: str, style: str):
        # Hook donde puedes conectar tu backend real
        # Por ejemplo: llamada a API para generar imagen y mintear NFT
        print(f"[DEBUG] Generando NFT con estilo='{style}' y prompt='{prompt[:60]}...'")

if __name__ == "__main__":
    app = App()
    app.mainloop()
