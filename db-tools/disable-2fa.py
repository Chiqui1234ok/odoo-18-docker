import os
import subprocess
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

try:
    # Solicitar el nombre de usuario de Odoo
    odoo_user = input("Introduce el nombre del usuario (login) de Odoo: ").strip()

    # Consulta SQL para verificar si el usuario tiene un secreto de 2FA configurado
    select_query = f"SELECT totp_secret FROM res_users WHERE login = '{odoo_user}';"
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
    totp_secret = subprocess.check_output(cmd_check_2fa, text=True).strip()

    if totp_secret == "":
        print(f"El usuario '{odoo_user}' no tiene 2FA activado (sin secreto configurado). No se requiere desactivación.")
    else:
        # Si ya tiene un secreto, desactivar el 2FA (borrar el secreto)
        print(f"El usuario '{odoo_user}' tiene 2FA activado. Se procederá a desactivarlo.")
        update_query = f"UPDATE res_users SET totp_secret = NULL WHERE login = '{odoo_user}';"
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

        subprocess.run(cmd_update_2fa, check=True)
        print(f"El 2FA para el usuario '{odoo_user}' ha sido desactivado correctamente.")

except subprocess.CalledProcessError as e:
    print(f"Error al ejecutar comandos en el contenedor Docker: {e}")
except Exception as e:
    print(f"Error: {e}")
