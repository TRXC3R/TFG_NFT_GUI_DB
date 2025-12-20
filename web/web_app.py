# web/web_app.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from database.supabase_db_manager import supabase  

app = FastAPI(title="NFT Gallery")

# 1) Endpoint JSON: imágenes de un usuario
@app.get("/api/users/{user_id}/images")
def get_user_images(user_id: int):
    resp = (
        supabase
        .table("images")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    data = resp.data or []
    return {"user_id": user_id, "count": len(data), "images": data}

# 2) Endpoint HTML: galería de imágenes de un usuario
@app.get("/gallery/{user_id}", response_class=HTMLResponse)
def gallery(user_id: int):
    resp = (
        supabase
        .table("images")
        .select("id, prompt, file_url, created_at")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    images = resp.data or []

    items_html = []
    for img in images:
        items_html.append(f"""
            <div style="display:inline-block;margin:10px;text-align:center;">
                <img src="{img['file_url']}" 
                     alt="{img['prompt']}" 
                     style="max-width:250px;max-height:250px;display:block;margin-bottom:5px;">
                <div style="font-size:12px;color:#ccc;">{img['prompt']}</div>
                <div style="font-size:11px;color:#888;">{img['created_at']}</div>
            </div>
        """)

    body = "".join(items_html) or "<p>No hay imágenes para este usuario.</p>"

    html = f"""
    <html>
      <head>
        <title>Galería de usuario {user_id}</title>
        <meta charset="utf-8">
        <style>
          body {{
            background:#111;
            color:#eee;
            font-family: system-ui, sans-serif;
            text-align:center;
          }}
        </style>
      </head>
      <body>
        <h1>Galería de usuario {user_id}</h1>
        {body}
      </body>
    </html>
    """
    return html
