import requests
import base64
import threading
import time
from pathlib import Path

BASE_URL = "http://127.0.0.1:7860"
OUTPUT_DIR = Path("./output_images")

class GenerationTask:
    #Representa una tarea de generación en progreso
    def __init__(self, task_id, user_id, prompt, style, num_steps):
        self.task_id = task_id
        self.user_id = user_id
        self.prompt = prompt
        self.style = style
        self.num_steps = num_steps
        self.progress = 0.0
        self.eta = 0
        self.status = "generating"  # generating, completed, failed, cancelled
        self.result_path = None
        self.error = None

# Registro de tareas en progreso
active_tasks = {}

def generate_image(user_id: int, prompt: str, style: str, num_steps: int, 
                   task_id: str) -> GenerationTask:
    """
    Genera imagen y la guarda en BD
    Se ejecuta en hilo aparte
    """
    task = GenerationTask(task_id, user_id, prompt, style, num_steps)
    active_tasks[task_id] = task
    
    try:
        # Preparar payload
        payload = {
            "prompt": f'{prompt}, {style} style',
            "steps": num_steps,
            "seed": -1  # Random seed
        }
        
        # Enviar a API
        response = requests.post(f'{BASE_URL}/sdapi/v1/txt2img', json=payload)
        response.raise_for_status()
        
        r = response.json()
        
        # Crear carpeta si no existe
        user_dir = OUTPUT_DIR / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)
        
        # Guardar imagen
        first_word = prompt.split()[0].lower()
        file_path = user_dir / f"{first_word}_{int(time.time())}.png"
        
        with open(file_path, 'wb') as f:
            f.write(base64.b64decode(r['images'][0]))
        
        task.progress = 1.0
        task.status = "completed"
        task.result_path = str(file_path)
        #task.image_id = image_id
        
        print(f"✅ Imagen guardada: {file_path}")
        return file_path
        
    except Exception as e:
        task.status = "failed"
        task.error = str(e)
        print(f"❌ Error generando imagen: {e}")
    
    # Limpiar tarea después de 5 minutos
    time.sleep(300)
    active_tasks.pop(task_id, None)

def start_generation(user_id: int, prompt: str, style: str, num_steps: int) -> str:
    """
    Inicia generación en hilo aparte
    Devuelve task_id para consultarlo
    """
    task_id = f"{user_id}_{int(time.time() * 1000)}"
    
    t = threading.Thread(
        target=generate_image,
        args=(user_id, prompt, style, num_steps, task_id),
        daemon=True
    )
    t.start()
    
    return task_id

def get_task_progress(task_id: str) -> dict:
    """Obtiene progreso de una tarea"""
    if task_id not in active_tasks:
        return {"error": "Task not found"}
    
    task = active_tasks[task_id]
    
    # Consultar endpoint de progreso de Stable Diffusion
    try:
        r = requests.get(f"{BASE_URL}/sdapi/v1/progress").json()
        progress = r.get("progress", 0.0)
        eta = r.get("eta_relative", 0)
        
        task.progress = progress
        task.eta = eta
    except:
        pass
    
    return {
        "task_id": task_id,
        "status": task.status,
        "progress": task.progress,
        "eta": task.eta,
        "error": task.error
    }

def get_task_result(task_id: str) -> dict:
    #Obtiene el resultado de una tarea completada
    if task_id not in active_tasks:
        return {"error": "Task not found"}
    
    task = active_tasks[task_id]
    
    if task.status == "completed":
        return {
            "success": True,
            "image_path": task.result_path,
            "image_id": task.image_id
        }
    elif task.status == "failed":
        return {"success": False, "error": task.error}
    else:
        return {"success": False, "error": "Task still processing"}
