import sys
import os
# Ajuste de path para que Docker encuentre los módulos correctamente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Optional

# Importaciones del proyecto
from src.Services.Gimnasio_service import GimnasioService
from src.schemas.schemas import SocioCreate, SocioResponse, ClaseCreate, ClaseResponse, Token
from src.models.Socio import Socio
from src.auth import create_access_token, decode_token  # Importamos auth

app = FastAPI(title="Gimnasio Inteligente API")
gym_service = GimnasioService()

# Endpoint para Swagger UI (Pide usuario/contraseña)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- AUTENTICACIÓN (Práctica 4) ---

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint estándar OAuth2 para obtener el token JWT.
    Username = email del socio
    Password = contraseña del socio
    """
    # Usamos el servicio para verificar credenciales de forma segura
    socio = gym_service.autenticar_socio(form_data.username, form_data.password)
    
    if not socio:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Si es correcto, generamos el token
    access_token = create_access_token(data={"sub": socio.email})
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependencia para proteger endpoints"""
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    email = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: no contiene email (sub)",
            headers={"WWW-Authenticate": "Bearer"},)
    
    socio_id = gym_service.email_socio_index.get(email)
    
    if not socio_id:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
        
    return gym_service.socios[socio_id]

# --- ENDPOINTS SOCIOS (Práctica 3) ---

@app.post("/socios", response_model=SocioResponse, status_code=201)
def registrar_socio(socio: SocioCreate):
    try:
        nuevo_socio = gym_service.registrar_socio(
            socio.nombre, 
            socio.email, 
            socio.fecha_nacimiento, 
            socio.nivel, 
            socio.password
        )
        return nuevo_socio
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/socios", response_model=List[SocioResponse])
def listar_socios(current_user: Socio = Depends(get_current_user)):
    """
    Devuelve todos los socios.
    Requiere token (candado en Swagger).
    """
    return gym_service.listar_socios()

@app.get("/socios/me", response_model=SocioResponse)
def leer_mi_perfil(current_user: Socio = Depends(get_current_user)):
    """Devuelve los datos del usuario logueado actualmente"""
    return current_user

# --- ENDPOINTS CLASES ---

@app.post("/clases", response_model=ClaseResponse)
def crear_clase(clase: ClaseCreate, current_user: Socio = Depends(get_current_user)):
    """Crea una nueva clase. Requiere autenticación."""
    try:
        # Nota: En un sistema real verificaríamos si current_user es admin/entrenador
        nueva = gym_service.crear_clase(
            clase.nombre, clase.horario, clase.aforo, clase.entrenador_id
        )
        # Preparamos la respuesta calculando plazas
        resp = vars(nueva)
        resp['plazas_disponibles'] = nueva.plazas_disponibles()
        return resp
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/clases", response_model=List[ClaseResponse])
def listar_clases():
    """Listar clases es público."""
    res = []
    for c in gym_service.listar_clases():
        d = vars(c)
        d['plazas_disponibles'] = c.plazas_disponibles()
        res.append(d)
    return res

# Endpoint de Health Check
@app.get("/")
def root():
    return {"mensaje": "API del Gimnasio Inteligente funcionando correctamente"}