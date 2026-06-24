from app.config import settings

print(f"DEBUG: Intentando conectar con:")
print(f"Usuario: {settings.DB_USER}")
print(f"Password: {settings.DB_PASSWORD}")
print(f"Host: {settings.DB_HOST}")
print(f"URL completa: {settings.DATABASE_URL}")