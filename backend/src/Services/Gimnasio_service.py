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
        if email in self.email_socio_index:
            raise ValueError(f"Error: el email {email} ya está registrado.")

        socio = Socio(nombre, email, fecha_nacimiento, nivel, password)
        self.socios[socio.id] = socio
        self.email_socio_index[email] = socio.id
        return socio

    def autenticar_socio(self, email: str, password_plana: str) -> Optional[Socio]:
        socio_id = self.email_socio_index.get(email)
        if not socio_id:
            return None
        
        socio = self.socios.get(socio_id)
        if socio and socio.verificar_contrasena(password_plana):
            return socio
        return None

    def listar_socios(self) -> List[Socio]:
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
        # 1. Validación de existencia del Entrenador (Mínima validación requerida)
        if entrenador_id not in self.entrenadores:
            # Esta línea se mantiene para la seguridad básica
            raise ValueError("Error: entrenador no encontrado.")

        # 2. Creación del objeto
        clase = Clase(nombre, horario, aforo, entrenador_id)
        
        # 3. PERSISTENCIA: Esta línea DEBE ser la única y la última antes del return.
        self.clases[clase.id] = clase
        
        # Eliminamos cualquier otra referencia o llamada de función aquí.
        
        return clase

    def listar_clases(self) -> List[Clase]:
        return list(self.clases.values())

    # --- AQUÍ ESTABAN LOS MÉTODOS QUE FALTABAN ---

    def reservar_clase(self, socio_id: str, clase_id: str) -> bool:
        """Reserva una clase para un socio."""
        socio = self.socios.get(socio_id)
        clase = self.clases.get(clase_id)

        if not socio or not clase:
            return False

        # Intentar inscribir en la clase (controla aforo)
        if clase.inscribir_socio(socio_id):
            socio.reservar_clase(clase_id)
            return True
        return False

    def cancelar_reserva_clase(self, socio_id: str, clase_id: str) -> bool:
        """Cancela una reserva."""
        socio = self.socios.get(socio_id)
        clase = self.clases.get(clase_id)

        if not socio or not clase:
            return False

        if clase.cancelar_reserva(socio_id):
            socio.cancelar_reserva(clase_id)
            return True
        return False

    # =========== GESTIÓN DE RUTINAS ===========
    
    def crear_rutina(self, nombre: str, duracion: int, dificultad: str) -> Rutina:
        rutina = Rutina(nombre, duracion, dificultad)
        self.rutinas[rutina.id] = rutina
        return rutina

    def listar_rutinas(self) -> List[Rutina]:
        """Retorna todas las rutinas."""
        return list(self.rutinas.values())

    def asignar_rutina(self, socio_id: str, rutina_id: str) -> bool:
        socio = self.socios.get(socio_id)
        rutina = self.rutinas.get(rutina_id)
        if socio and rutina:
            socio.asignar_rutina(rutina_id)
            return True
        return False

    # =========== GESTIÓN DE PROGRESO, IoT y ACCESOS ===========

    def registrar_progreso(self, socio_id: str, peso: float, repeticiones: int, tiempo: int) -> Progreso:
        if socio_id not in self.socios:
            raise ValueError("Socio no encontrado")
        progreso = Progreso(socio_id, peso, repeticiones, tiempo)
        self.progresos[progreso.id] = progreso
        self.socios[socio_id].registrar_progreso(progreso.id)
        return progreso
    
    def listar_progresos_socio(self, socio_id: str) -> List[Progreso]:
        """Retorna el historial de progresos de un socio."""
        socio = self.socios.get(socio_id)
        if not socio:
            return []

        # Busca los objetos Progreso reales usando los IDs guardados en el socio
        historial = []
        for prog_id in socio.progresos:
            if prog_id in self.progresos:
                historial.append(self.progresos[prog_id])
        
        return historial

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