import psycopg2
import os

# Forzamos la codificación a nivel de sistema antes de que el driver cargue
os.environ["LANG"] = "en_US.UTF-8"
os.environ["LC_ALL"] = "en_US.UTF-8"

try:
    # Agregamos 'options' para forzar el idioma de los mensajes
    conn = psycopg2.connect(
        dbname="presupuesto_db",
        user="postgres",
        password="supersecretpassword",
        host="127.0.0.1",
        port="5432",
        options="-c lc_messages=C"
    )
    print("¡CONEXIÓN EXITOSA!")
    conn.close()
except Exception as e:
    print(f"Error técnico: {e}")