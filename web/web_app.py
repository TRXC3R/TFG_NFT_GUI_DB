from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from database.db_manager import db

app = FastAPI()

OUTPUT_DIR = Path("./output_images")
app.mount("/output_images", StaticFiles(directory=OUTPUT_DIR), name="output_images")

@app.get("/gallery", response_class=HTMLResponse)
async def gallery():
    images = db.get_all_images(limit=500)  # ya tienes este método en db_manager
    html_items = []
    for img in images:
        html_items.append(
            f"""
            <div style="margin:10px;display:inline-block;text-align:center;">
                <img src="{img['file_path']}" alt="{img['prompt']}" style="max-width:200px;"><br>
                <small>{img['prompt']}</small><br>
                <small>by {img.get('username','')}</small>
            </div>
            """
        )

    html = f"""
    <html>
    <head><title>Galería de NFTs</title></head>
    <body>
        <h1>Galería de imágenes generadas</h1>
        {''.join(html_items)}
    </body>
    </html>
    """
    return html
