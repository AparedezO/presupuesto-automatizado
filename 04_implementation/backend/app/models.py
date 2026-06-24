from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Material(Base):
    __tablename__ = "materiales"

    # Llave primaria indexada automáticamente
    id = Column(Integer, primary_key=True, index=True)
    
    # Campos base mapeados del Excel maestro
    codigo = Column(String, unique=True, index=True, nullable=False)
    descripcion = Column(String, nullable=False)
    unidad = Column(String, nullable=False)
    precio_unitario = Column(Float, nullable=False, default=0.0)
    
    # Campo clave SRE: Estado de sincronización diferida
    # Estados posibles: 'sincronizado', 'pendiente_sync'
    estado_sync = Column(String, default="pendiente_sync", index=True)
    
    # Auditoría: Saber exactamente cuándo se creó o modificó el registro en caliente
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), onupdate=func.now())