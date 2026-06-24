import psycopg2
try:
    conn = psycopg2.connect(
        dbname="presupuesto_db",
        user="postgres",
        password="supersecretpassword",
        host="127.0.0.1",
        port="5432"
    )
    print("¡CONEXIÓN EXITOSA!")
    conn.close()
except Exception as e:
    print(f"Error detectado: {e}")