import os
import subprocess
from dotenv import load_dotenv

# Cargar las variables del archivo .env
def load_env():
    if not os.path.exists(".env"):
        print("Archivo .env no encontrado")
        return False
    load_dotenv()
    return True

# Verificar si las variables necesarias están configuradas
def validate_env():
    required_vars = ["POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD"]
    missing_vars = [var for var in required_vars if var not in os.environ]
    if missing_vars:
        print(f"Faltan las siguientes variables en el archivo .env: {', '.join(missing_vars)}")
        return False
    return True

# Ejecutar el comando para conectarse al contenedor
def connect_to_postgres():
    container_name = "postgre"  # Nombre del contenedor Docker
    postgres_db = os.getenv("POSTGRES_DB")
    postgres_user = os.getenv("POSTGRES_USER")

    try:
        subprocess.run(
            ["docker", "exec", "-it", container_name, "psql", "-U", postgres_user, "-d", postgres_db],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error al intentar conectarse: {e}")

def main():
    if not load_env():
        return
    if not validate_env():
        return
    connect_to_postgres()

if __name__ == "__main__":
    main()
