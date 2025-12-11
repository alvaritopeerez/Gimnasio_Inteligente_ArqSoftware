import sys
import os
# Ajuste de path para que Docker encuentre los módulos correctamente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Optional

# Importaciones del proyecto
from src.Services.Gimnasio_service import GimnasioService
from src.schemas.schemas import (
    SocioCreate, SocioResponse, 
    ClaseCreate, ClaseResponse, 
    Token, ReservaRequest, 
    RutinaResponse, RutinaCreate,
    EntrenadorCreate, EntrenadorResponse
)
from src.models.Socio import Socio
from src.models.DispositivoIoT import DispositivoIoT 
from src.auth import create_access_token, decode_token  # Importamos auth

app = FastAPI(title="Gimnasio Inteligente API")
gym_service = GimnasioService()

# --- EVENTO DE INICIO: CARGA DE DATOS AUTOMÁTICA ---
@app.on_event("startup")
def startup_event():
    """Inicializa el gimnasio con datos de prueba al arrancar."""
    print("🚀 Arrancando sistema... Verificando datos iniciales...")
    
    # 1. Chequear si ya hay datos (por si implementas persistencia futura)
    if not gym_service.listar_entrenadores():
        print("⚡ Base de datos vacía. Creando datos semilla...")
        
        # A) Crear Entrenadores
        e1 = gym_service.registrar_entrenador("Yago Fontenla", "yago@gym.com", "CrossFit")
        e2 = gym_service.registrar_entrenador("Ana López", "ana@gym.com", "Yoga")
        
        # B) Crear Clases (Usando los IDs de los entrenadores creados)
        gym_service.crear_clase("Yoga Matutino", "08:00", 15, e2.id)
        gym_service.crear_clase("CrossFit Duro", "18:00", 10, e1.id)
        gym_service.crear_clase("Pilates Core", "19:30", 12, e2.id)
        
        # C) Crear Rutinas
        gym_service.crear_rutina("Fuerza Básica", 45, "principiante")
        gym_service.crear_rutina("Cardio HIIT", 30, "avanzado")
        
        # D) Crear un Usuario Admin/Demo (Opcional, para entrar rápido)
        # gym_service.registrar_socio("Admin Demo", "admin@gym.com", "1990-01-01", "avanzado", "1234")

        # E) Crear Dispositivo IoT de Demo
        demo_device = DispositivoIoT(tipo="pulsera", socio_id="demo_user")
        demo_device.id = "pulsera-web"  # Forzamos el ID que busca el frontend
        gym_service.dispositivos["pulsera-web"] = demo_device
        
        print("✅ Datos iniciales cargados correctamente.")
    else:
        print("👍 El sistema ya tiene datos.")

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

# --- ENDPOINTS ENTRENADORES ---

@app.post("/entrenadores", response_model=EntrenadorResponse, status_code=201)
def registrar_entrenador(entrenador: EntrenadorCreate):
    try:
        return gym_service.registrar_entrenador(
            entrenador.nombre, 
            entrenador.email, 
            entrenador.especialidad
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/entrenadores", response_model=List[EntrenadorResponse])
def listar_entrenadores():
    return gym_service.listar_entrenadores()

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
        # Usamos .copy() para no modificar el objeto original en memoria
        d = vars(c).copy() 
        # Calculamos el campo extra
        d['plazas_disponibles'] = c.plazas_disponibles()
        res.append(d)
    return res

@app.post("/reservas", status_code=201)
def reservar_clase(reserva: ReservaRequest, current_user: Socio = Depends(get_current_user)):
    """Permite a un socio reservar una clase."""
    try:
        exito = gym_service.reservar_clase(current_user.id, reserva.clase_id)
        if not exito:
            raise HTTPException(status_code=400, detail="No se pudo reservar (clase llena, usuario no encontrado o ya inscrito).")
        return {"mensaje": "Reserva realizada con éxito"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/reservas/{clase_id}")
def cancelar_reserva(clase_id: str, current_user: Socio = Depends(get_current_user)):
    """Permite cancelar una reserva."""
    exito = gym_service.cancelar_reserva_clase(current_user.id, clase_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Reserva no encontrada o no se pudo cancelar")
    return {"mensaje": "Reserva cancelada correctamente"}

# --- ENDPOINTS RUTINAS (NUEVO) ---

@app.post("/rutinas", response_model=RutinaResponse, status_code=201)
def crear_rutina(rutina: RutinaCreate):
    """Crea una nueva rutina en el sistema."""
    nueva_rutina = gym_service.crear_rutina(
        rutina.nombre, 
        rutina.duracion, 
        rutina.dificultad
    )
    return nueva_rutina

@app.get("/rutinas", response_model=List[RutinaResponse])
def listar_rutinas():
    """Devuelve todas las rutinas disponibles."""
    return gym_service.listar_rutinas()

@app.get("/rutinas/me", response_model=List[RutinaResponse])
def listar_mis_rutinas(current_user: Socio = Depends(get_current_user)):
    """Devuelve las rutinas asignadas al usuario logueado."""
    mis_rutinas = []
    # Recorremos los IDs de rutinas que tiene el socio guardados
    for rutina_id in current_user.rutinas:
        # Buscamos el objeto Rutina real en el diccionario del servicio
        rutina = gym_service.rutinas.get(rutina_id)
        if rutina:
            mis_rutinas.append(rutina)
    return mis_rutinas

@app.post("/rutinas/{rutina_id}/asignar")
def asignar_rutina(rutina_id: str, current_user: Socio = Depends(get_current_user)):
    """Asigna una rutina al usuario logueado."""
    try:
        gym_service.asignar_rutina(current_user.id, rutina_id)
        return {"mensaje": "Rutina asignada a tu plan de entrenamiento"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/iot/sincronizar/{dispositivo_id}")
@app.post("/iot/sincronizar/{dispositivo_id}")
def sincronizar_dispositivo(dispositivo_id: str, current_user: Socio = Depends(get_current_user)):
    """
    Simula la sincronización de un dispositivo IoT y registra el progreso automáticamente.
    (Alineado con el Diagrama de Secuencia: Sincronizar -> Validar -> Registrar Progreso)
    """
    # 1. Llamada al servicio para obtener los datos crudos del dispositivo
    datos = gym_service.sincronizar_dispositivo(dispositivo_id)
    
    if not datos:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado o error de conexión")
    
    # 2. Lógica de Mapeo y Persistencia Automática
    try:
        # Inicializamos variables para el modelo Progreso
        peso_reg = 0.0
        reps_reg = 0
        tiempo_reg = 0
        guardar_registro = False

        # ANALIZAMOS LOS DATOS RECIBIDOS SEGÚN EL TIPO DE DISPOSITIVO
        # (Ver src/models/DispositivoIoT.py para las claves del diccionario)

        # CASO A: Sensor de Fuerza (Ej: Máquina de gimnasio)
        if "peso_levantado" in datos and "repeticiones" in datos:
            peso_reg = float(datos.get("peso_levantado", 0))
            reps_reg = int(datos.get("repeticiones", 0))
            tiempo_reg = int(datos.get("tiempo_ejercicio", 0))
            guardar_registro = True

        # CASO B: Báscula Inteligente
        elif "peso" in datos:
            peso_reg = float(datos.get("peso", 0))
            # Repeticiones y tiempo se quedan en 0 porque es una medida corporal
            guardar_registro = True

        # CASO C: Pulsera (Opcional)
        # Aunque la pulsera da pasos/calorías, el modelo Progreso actual pide Peso/Reps/Tiempo.
        # Podríamos mapear 'tiempo_ejercicio' si viniera de una actividad.
        # Por ahora, solo registramos si hay datos compatibles con el modelo actual.

        # 3. Registrar en el sistema (Persistencia)
        if guardar_registro:
            gym_service.registrar_progreso(
                socio_id=current_user.id,
                peso=peso_reg,
                repeticiones=reps_reg,
                tiempo=tiempo_reg
            )
            mensaje_extra = " y progreso guardado en historial."
        else:
            mensaje_extra = " (datos informativos, no guardados en progreso)."

    except ValueError as e:
        print(f"Error validando datos IoT: {e}")
        # No fallamos la petición entera, pero avisamos que no se guardó el histórico
        mensaje_extra = " pero hubo un error al guardar el progreso."

    return {
        "mensaje": f"Sincronización exitosa{mensaje_extra}", 
        "datos_recibidos": datos
    }

@app.post("/accesos")
def registrar_acceso_gym(current_user: Socio = Depends(get_current_user)):
    """Registra que el usuario acaba de entrar al gimnasio (Torno)."""
    try:
        acceso = gym_service.registrar_acceso(current_user.id)
        return {"mensaje": "Acceso permitido", "detalle": str(acceso)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/progreso")
def ver_mi_progreso(current_user: Socio = Depends(get_current_user)):
    """Devuelve el historial real de progreso para las gráficas."""
    # Nota: Necesitarías añadir un método 'listar_progresos_socio' en el servicio 
    # o acceder directo si es sencillo, pero para el prototipo esto cumple.
    return gym_service.listar_progresos_socio(current_user.id)

# Endpoint de Health Check
@app.get("/")
def root():
    return {"mensaje": "API del Gimnasio Inteligente funcionando correctamente"}