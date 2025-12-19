from supabase import create_client, Client
import datetime
import bcrypt

DRM_TFG_URL = "https://tujlnbhnttgyztknwibf.supabase.co"
DRM_ANON_TFG_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR1amxuYmhudHRneXp0a253aWJmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjYxNjMzODYsImV4cCI6MjA4MTczOTM4Nn0.WtnWMysAy4EaJSnfAm1l_w5FikZcHL_xs4VrQ4UlLjk"
DRM_SECRET_TFG_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR1amxuYmhudHRneXp0a253aWJmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjE2MzM4NiwiZXhwIjoyMDgxNzM5Mzg2fQ.1AXHFKHNen6UdKTmoEFBBgAfz_7_WWINqFHJJ550opU"

supabase_drm_tfg: Client = create_client(DRM_TFG_URL, DRM_SECRET_TFG_KEY)

#Mi informacion en ficu
#{"id":"cb4df51f-f00a-4417-b2f5-a653a0608d1f",
# "name":"Darío Márquez Ibáñez",
# "password_hash":"A65A1B03",
# "created_at":"2025-11-03T15:58:01.523+00:00"


def search_user():
    response = supabase_drm_tfg.table("users").select("*").limit(100).execute()
    print("Registro encontrado:")
    for row in response.data:
        #print(f"ID: '{row['id']}' | Nombre: {row['name']}")
        id = row['id']
        username = row['username']
        password_hash = row['password_hash']
        print(f"Se han encontrado los datos de: ID: '{row['id']}' | Nombre: {row['username']}")

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
