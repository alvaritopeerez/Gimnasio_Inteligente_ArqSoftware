from pydantic import BaseModel, EmailStr
from typing import Optional, List

# Auth
class Token(BaseModel):
    access_token: str
    token_type: str

# Socio
class SocioCreate(BaseModel):
    nombre: str
    email: EmailStr
    fecha_nacimiento: str
    nivel: str = "principiante"
    password: str

class SocioResponse(BaseModel):
    id: str
    nombre: str
    email: EmailStr
    nivel: str
    
    class Config:
        from_attributes = True

# Clase
class ClaseCreate(BaseModel):
    nombre: str
    horario: str
    aforo: int
    entrenador_id: str

class ClaseResponse(BaseModel):
    id: str
    nombre: str
    horario: str
    aforo: int
    plazas_disponibles: int