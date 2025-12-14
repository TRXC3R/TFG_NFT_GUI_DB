import requests
import time
import base64
import threading

BASE_URL = "http://127.0.0.1:7860"


progress = 0

def start_generation_thread(prompt, style, num_steps, username):
    # Desactivar botón para evitar clicks repetidos
    #self.btn.configure(state="disabled")
    t = threading.Thread(target=generate_image, args=(prompt, style, num_steps, username), daemon=True)
    t.start()
    # Empieza a consultar progreso
    #report_progress()

def generate_image(prompt, style, num_steps, username):
# Define the URL and the payload to send.
   
    #https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/API
    payload = {
        "prompt": f'{prompt}, {style} style',
        "steps": num_steps
    }

    # Send said payload to said URL through the API.
    response = requests.post(url=f'{BASE_URL}/sdapi/v1/txt2img', json=payload)
    r = response.json()

    first_name = prompt.split(' ')[0] # Get the first word of the prompt to use as filename.
    ruta_imagen_output = f"./output_images/{username}/{first_name}.png"

    # Decode and save the image.
    with open(ruta_imagen_output, 'wb') as f:
        f.write(base64.b64decode(r['images'][0]))

    return ruta_imagen_output

def report_progress():
    try:
        r = requests.get(f"{BASE_URL}/sdapi/v1/progress", params={"skip_current_image": True}).json()
        prog = r.get("progress", 0.0)
        
        # Imprimir el progreso
        print(f"Progreso: {prog * 100:.1f}%")
        
        if prog < 1.0:
            time.sleep(0.5)  # espera 500ms antes de volver a preguntar
            report_progress()  # llamada recursiva
        else:
            print("¡Imagen generada!")
    except Exception as e:
        print(f"Error: {e}")