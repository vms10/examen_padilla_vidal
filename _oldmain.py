# archivo principal
import os
from fastapi import FastAPI, File, UploadFile,HTTPException
from fastapi.responses import FileResponse
from typing import Annotated
app = FastAPI()

@app.get("/hola")
async def prueba_root():
    return {"message": "Accediste al endpoint de prueba"}

@app.get("/files")
async def buscar_archivos():
    carpeta = "files"

    # Verifica que la carpeta exista
    if not os.path.exists(carpeta):
        return {"error": f"La carpeta '{carpeta}' no existe."}

    # Lista solo los archivos dentro de la carpeta
    archivos = [
        f for f in os.listdir(carpeta)
        if os.path.isfile(os.path.join(carpeta, f))
    ]
    return {"archivos": archivos}






# Endpoint que guarda el archivo en la carpeta "files"
@app.post("/files")
async def upload_file(
    file: Annotated[UploadFile, File(...)]
):
    # Asegurarte de que exista la carpeta "files"
    os.makedirs("files", exist_ok=True)

    # Ruta completa donde se va a guardar
    save_path = os.path.join("files", os.path.basename(file.filename))

    # Leer el contenido del archivo y escribirlo
    with open(save_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return {"message": f"Archivo guardado como {save_path}", "size": len(content)}

# te descarga el archivo
@app.get("/files/{file_name}")
async def contenido_archivo(file_name:str):
    path = os.path.join("files", file_name)  # carpeta hardcodeada
    if not os.path.exists(path) or not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    # Fuerza descarga con nombre del archivo
    return FileResponse(path, media_type="application/octet-stream", filename=file_name)




