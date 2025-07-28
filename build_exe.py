
import os
import subprocess
import sys

# Cambiar al directorio del proyecto
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Ruta al archivo principal
archivo_principal = "main.py"
nombre_exe = "mi_app"

# Formato de --add-data depende del sistema operativo
sep = ";" if sys.platform == "win32" else ":"

# Archivos adicionales que deben incluirse
add_data = [
    f"mi_base.db{sep}.",                        # base de datos sqlite
]

# Comando base
comando = [
    "pyinstaller",
    "--name", nombre_exe,
    "--onefile",
    "--windowed",
]

# Agregar archivos adicionales con --add-data
for data in add_data:
    comando += ["--add-data", data]

# Archivo principal
comando.append(archivo_principal)

print("Compilando con pyinstaller...
")
subprocess.run(comando)
print("\n✅ ¡Listo! El .exe estará en /dist/")
