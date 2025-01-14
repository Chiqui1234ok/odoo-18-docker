import os
import subprocess
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

try:
    # Solicitar el nombre de usuario de Odoo
    odoo_user = input("Introduce el nombre del usuario (login) de Odoo: ").strip()

    # Consulta SQL para verificar si el usuario tiene habilitado el 2FA
    select_query = f"SELECT totp_enabled FROM res_users WHERE login = '{odoo_user}';"
    cmd_check_2fa = [
        "docker",
        "exec",
        "-i",
        os.getenv("POSTGRES_CONTAINER_NAME"),
        "psql",
        "-U",
        os.getenv("POSTGRES_USER"),
        "-d",
        os.getenv("POSTGRES_DB"),
        "-t",
        "-c",
        select_query,
    ]

    # Ejecutar comando para verificar el estado de 2FA
    totp_status = subprocess.check_output(cmd_check_2fa, text=True).strip()

    if totp_status == "":
        print(f"El usuario '{odoo_user}' no se encuentra en la base de datos.")
    else:
        current_status = totp_status.lower() == 't'  # PostgreSQL devuelve 't' para true y 'f' para false
        new_status = not current_status

        print(f"Estado actual del 2FA para '{odoo_user}': {'Activado' if current_status else 'Desactivado'}")
        print(f"El 2FA será {'Activado' if new_status else 'Desactivado'}.")

        # Consulta SQL para cambiar el estado de 2FA
        update_query = f"UPDATE res_users SET totp_enabled = {'TRUE' if new_status else 'FALSE'} WHERE login = '{odoo_user}';"
        cmd_update_2fa = [
            "docker",
            "exec",
            "-i",
            os.getenv("POSTGRES_CONTAINER_NAME"),
            "psql",
            "-U",
            os.getenv("POSTGRES_USER"),
            "-d",
            os.getenv("POSTGRES_DB"),
            "-c",
            update_query,
        ]

        # Ejecutar comando para actualizar el estado de 2FA
        subprocess.run(cmd_update_2fa, check=True)
        print(f"El 2FA para el usuario '{odoo_user}' ha sido {'activado' if new_status else 'desactivado'} correctamente.")

except subprocess.CalledProcessError as e:
    print(f"Error al ejecutar comandos en el contenedor Docker: {e}")
except Exception as e:
    print(f"Error: {e}")
