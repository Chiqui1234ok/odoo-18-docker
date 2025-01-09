import os
from dotenv import load_dotenv

# ATENCIÓN: ESTE SCRIPT NECESITA ARCHIVO ".env"
load_dotenv()
print(f"ODOO_CONTAINER_NAME: {os.getenv('ODOO_CONTAINER_NAME')}")
print(f"POSTGRES_CONTAINER_NAME: {os.getenv('POSTGRES_CONTAINER_NAME')}")
print(f"POSTGRES_DB: {os.getenv('POSTGRES_DB')}")
print(f"POSTGRES_HOST: {os.getenv('POSTGRES_HOST')}")
print(f"POSTGRES_PORT: {os.getenv('POSTGRES_PORT')}")
print(f"POSTGRES_USER: {os.getenv('POSTGRES_USER')}")
print(f"POSTGRES_PASSWORD: {os.getenv('POSTGRES_PASSWORD')}")