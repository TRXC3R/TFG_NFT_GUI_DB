from supabase import create_client, Client
import datetime
import bcrypt

DRM_TFG_URL = "https://tujlnbhnttgyztknwibf.supabase.co"
DRM_ANON_TFG_KEY = ""
DRM_SECRET_TFG_KEY = ""

supabase_drm_tfg: Client = create_client(DRM_TFG_URL, DRM_SECRET_TFG_KEY)


#Funcion que busca un usuario por su ID y devuelve su nombre de usuario
def search_user(username):
    response = supabase_drm_tfg.table("users").select("*").eq("username", username).execute()
    print("Registro encontrado:")
    for row in response.data:
        user_id = row['id']
        password_hash = row['password_hash']
        print(f"Se han encontrado los datos de: ID: '{row['id']}' | Nombre: {row['username']}")
    return user_id

def check_user_credentials_old(username, password):
    
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    print(f"[DEBUG] Hash de la contraseña para verificación: {password_hash}")

    response = (
        supabase_drm_tfg
        .table("users")
        .select("*")
        .eq("username", username)
        .eq("password_hash", password_hash)
        .execute()
    )

    if response.data:
        print(f"[DEBUG] Usuario '{username}' autenticado correctamente en Supabase.")
        return True
    else:
        print(f"[DEBUG] Fallo de autenticación para el usuario '{username}' en Supabase.")
        print(f"[DEBUG] Datos recibidos: {response.data}")
        return False


def check_user_credentials(username: str, password: str):
    # 1. Buscar solo por username para asegurarnos de que el usuario existe en la base de datos
    response = (
        supabase_drm_tfg
        .table("users")
        .select("*")
        .eq("username", username)
        .single()   # queremos solo un usuario
        .execute()
    )

    if not response.data:
        print("[DEBUG] Usuario no encontrado")
        return None  # o False
    else:
        print(f"[DEBUG] Usuario '{username}' encontrado en la base de datos.")

    user = response.data
    stored_hash = user["password_hash"]  # hash guardado en Supabase (string)

    # 2. Comparar con bcrypt.checkpw
    is_valid = bcrypt.checkpw(
        password.encode("utf-8"),
        stored_hash.encode("utf-8")
    )
    if not is_valid:
        print("[DEBUG] Contraseña incorrecta")
        return None  # o False
    print("[DEBUG] La Contraseña correcta")

    # 3. Devolver lo que necesites (id, username, etc.)
    return True

def create_tfg_user(id, username, password):

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    new_tfg_user = {
        "id": id,
        "username": username,
        "password_hash": password_hash
    }
    
    resp = (
        supabase_drm_tfg
        .table("users")
        .insert(new_tfg_user)     # también puedes pasar [new_tfg_user] como lista
        .execute()
    )

    # print(resp.data)

def upload_image_metadata(user_id: str, prompt: str, file_url: str):
    new_image = {
        "user_id": user_id,
        "prompt": prompt,
        "file_url": file_url,
    }

    resp = (
        supabase_drm_tfg
        .table("images")
        .insert(new_image)
        .execute()
    )

    print(f"[DEBUG] Metadatos de imagen subidos para el usuario {user_id}: {resp.data}")
