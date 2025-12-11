from typing import List, Dict, Optional, Any
from src.models.Socio import Socio
from src.models.Entrenador import Entrenador
from src.models.Clase import Clase
from src.models.Rutina import Rutina
from src.models.Progreso import Progreso
from src.models.DispositivoIoT import DispositivoIoT
from src.models.Acceso import Acceso

class GimnasioService:
    """Servicio que gestiona todas las operaciones del gimnasio."""

    def __init__(self) -> None:
        self.socios: Dict[str, Socio] = {}
        self.entrenadores: Dict[str, Entrenador] = {}
        self.clases: Dict[str, Clase] = {}
        self.rutinas: Dict[str, Rutina] = {}
        self.progresos: Dict[str, Progreso] = {}
        self.dispositivos: Dict[str, DispositivoIoT] = {}
        self.accesos: Dict[str, Acceso] = {}

        # Índices para búsqueda rápida
        self.email_socio_index: Dict[str, str] = {}
        self.email_entrenador_index: Dict[str, str] = {}

    # =========== GESTIÓN DE SOCIOS Y AUTENTICACIÓN ===========

    def registrar_socio(self, nombre: str, email: str, fecha_nacimiento: str, nivel: str, password: str) -> Socio:
        """Registra un nuevo socio guardando su contraseña de forma segura."""
        if email in self.email_socio_index:
            raise ValueError(f"Error: el email {email} ya está registrado.")

        # Creamos el socio (el modelo Socio se encarga de hashear la password)
        socio = Socio(nombre, email, fecha_nacimiento, nivel, password)
        
        self.socios[socio.id] = socio
        self.email_socio_index[email] = socio.id
        return socio

    def autenticar_socio(self, email: str, password_plana: str) -> Optional[Socio]:
        """
        Verifica las credenciales. Devuelve el objeto Socio si son correctas, 
        o None si fallan.
        """
        socio_id = self.email_socio_index.get(email)
        if not socio_id:
            return None
        
        socio = self.socios.get(socio_id)
        # Usamos el método seguro definido en models/Socio.py
        if socio and socio.verificar_contrasena(password_plana):
            return socio
        return None

    def listar_socios(self) -> List[Socio]:
        """Retorna lista de todos los socios."""
        return list(self.socios.values())

    def buscar_socio_por_id(self, socio_id: str) -> Optional[Socio]:
        return self.socios.get(socio_id)

    # =========== GESTIÓN DE ENTRENADORES ===========

    def registrar_entrenador(self, nombre: str, email: str, especialidad: str) -> Entrenador:
        if email in self.email_entrenador_index:
            raise ValueError(f"Error: el email {email} ya está registrado.")

        entrenador = Entrenador(nombre, email, especialidad)
        self.entrenadores[entrenador.id] = entrenador
        self.email_entrenador_index[email] = entrenador.id
        return entrenador

    def listar_entrenadores(self) -> List[Entrenador]:
        return list(self.entrenadores.values())

    # =========== GESTIÓN DE CLASES ===========

    def crear_clase(self, nombre: str, horario: str, aforo: int, entrenador_id: str) -> Clase:
        if entrenador_id not in self.entrenadores:
            raise ValueError("Error: entrenador no encontrado.")

        clase = Clase(nombre, horario, aforo, entrenador_id)
        self.clases[clase.id] = clase
        
        # Vincular al entrenador
        entrenador = self.entrenadores[entrenador_id]
        entrenador.crear_clase(clase.id)
        
        return clase

    def listar_clases(self) -> List[Clase]:
        return list(self.clases.values())

    # =========== GESTIÓN DE RUTINAS, PROGRESO, IoT, ACCESOS ===========
    # (El resto de métodos se mantienen igual que en tu lógica original)
    
    def crear_rutina(self, nombre: str, duracion: int, dificultad: str) -> Rutina:
        rutina = Rutina(nombre, duracion, dificultad)
        self.rutinas[rutina.id] = rutina
        return rutina

    def asignar_rutina(self, socio_id: str, rutina_id: str) -> bool:
        socio = self.socios.get(socio_id)
        rutina = self.rutinas.get(rutina_id)
        if socio and rutina:
            socio.asignar_rutina(rutina_id)
            return True
        return False

    def registrar_progreso(self, socio_id: str, peso: float, repeticiones: int, tiempo: int) -> Progreso:
        if socio_id not in self.socios:
            raise ValueError("Socio no encontrado")
        progreso = Progreso(socio_id, peso, repeticiones, tiempo)
        self.progresos[progreso.id] = progreso
        self.socios[socio_id].registrar_progreso(progreso.id)
        return progreso

    def registrar_dispositivo(self, tipo: str, socio_id: str) -> DispositivoIoT:
        if socio_id not in self.socios:
            raise ValueError("Socio no encontrado")
        dispositivo = DispositivoIoT(tipo, socio_id)
        self.dispositivos[dispositivo.id] = dispositivo
        return dispositivo

    def sincronizar_dispositivo(self, dispositivo_id: str) -> Optional[Dict]:
        dispositivo = self.dispositivos.get(dispositivo_id)
        if dispositivo:
            dispositivo.sincronizar()
            return dispositivo.datos
        return None

    def registrar_acceso(self, socio_id: str) -> Acceso:
        socio = self.socios.get(socio_id)
        if not socio:
            raise ValueError("Socio no encontrado")
        acceso = Acceso(socio_id, socio.nombre)
        self.accesos[acceso.id] = acceso
        return acceso