import os
import subprocess
from passlib.context import CryptContext
from getpass import getpass

# Configuración de variables
DB_CONTAINER = "db"  # Nombre del contenedor Docker para PostgreSQL

# Crear el contexto de hash para Odoo
pwd_context = CryptContext(schemes=["pbkdf2_sha512"], deprecated="auto")

try:
    # Solicitar el nombre de usuario
    odoo_user = input("Introduce el nombre del usuario (login) de Odoo: ").strip()

    # Verificar si el usuario existe en PostgreSQL dentro del contenedor
    select_query = f"SELECT id FROM res_users WHERE login = '{odoo_user}';"
    cmd_check_user = [
        "docker",
        "exec",
        "-i",
        DB_CONTAINER,
        "psql",
        "-U",
        os.getenv("POSTGRES_USER"),
        "-d",
        os.getenv("POSTGRES_DB"),
        "-t",
        "-c",
        select_query,
    ]

    # Ejecutar el comando para verificar el usuario
    user_id = subprocess.check_output(cmd_check_user, text=True).strip()

    if not user_id:
        print(f"El usuario '{odoo_user}' no se encuentra en la base de datos.")
    else:
        # Si el usuario existe, solicitar la nueva contraseña
        new_password = getpass("Introduce la nueva contraseña: ")

        # Generar el hash de la nueva contraseña
        hashed_password = pwd_context.hash(new_password)

        # Ejecutar el comando para actualizar la contraseña
        update_query = f"UPDATE res_users SET password = '{hashed_password}' WHERE login = '{odoo_user}';"
        cmd_update_password = [
            "docker",
            "exec",
            "-i",
            DB_CONTAINER,
            "psql",
            "-U",
            os.getenv("POSTGRES_USER"),
            "-d",
            os.getenv("POSTGRES_DB"),
            "-c",
            update_query,
        ]

        subprocess.run(cmd_update_password, check=True)
        print(f"Contraseña para el usuario '{odoo_user}' actualizada correctamente.")

except subprocess.CalledProcessError as e:
    print(f"Error al ejecutar comandos en el contenedor Docker: {e}")
except Exception as e:
    print(f"Error: {e}")
