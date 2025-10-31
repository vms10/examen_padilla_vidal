# 💳 API de Pagos - FastAPI
Marco Padilla y Maria Sol Vidal
---

## ⚙️ Set-up del entorno virtual

```bash
# Crear entorno virtual
python -m venv env

# Activar entorno virtual (Windows)
.\env\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

# 🚀 Levantar el servidor localmente
```bash
fastapi dev main.py
```

Una vez iniciado, podés acceder y probarlo localmente desde:

🌐 Servidor: http://127.0.0.1:8000

📘 Documentación interactiva: http://127.0.0.1:8000/docs

Obs: el enlace puede variar, va a aparecer en la consula al correr el comando de `fastapi`

# 🧪 Ejecutar los tests
Podes probar los unit tests localmente de la siguiente forma:
```bash
python -m unittest test_app.py
```
# 🐙 Workflows de github
## CI
En  `./github/workflows/ci_pipeline.yml` configuramos para correr automáticamente estos mismos unit_tests cada vez que querramos integrarnos a la branch `main`. También en el CI se instalan los requirements.
## CD
Configuramos en  `./github/workflows/cd_pipeline.yml` para crear un release cada vez que pusheamos un tag. Los comandos para hacer esto son:
```bash
git tag -a v1.0.0 -m "Primera versión estable"
git push origin v1.0.0
```
# 📦 Generar el archivo requirements.txt
De instalar nuevos paquetes se puede actualizar el archivo `requirements.txt` de la siguiente forma:
```bash
pip list
pip freeze > requirements.txt
```

# ☁️ Despliegue en Render

🔗 https://apifast-m5ay.onrender.com
