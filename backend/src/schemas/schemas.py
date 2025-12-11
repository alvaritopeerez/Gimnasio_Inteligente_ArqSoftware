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
    fecha_nacimiento: str
    
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
    
    class Config:
        from_attributes = True
        extra = "ignore"
    
class ReservaRequest(BaseModel):
    clase_id: str

class RutinaResponse(BaseModel):
    id: str
    nombre: str
    duracion: int
    dificultad: str
    
    class Config:
        from_attributes = True

class RutinaCreate(BaseModel):
    nombre: str
    duracion: int
    dificultad: str

# Entrenadores
class EntrenadorCreate(BaseModel):
    nombre: str
    email: EmailStr
    especialidad: str

class EntrenadorResponse(BaseModel):
    id: str
    nombre: str
    especialidad: str
    
    class Config:
        from_attributes = True