import uuid
from datetime import datetime
from typing import Optional

class Acceso:
    """Registro de acceso de un socio al gimnasio."""

    def __init__(self, socio_id: str, socio_nombre: Optional[str] = None):
        """
        Inicializa un registro de acceso.

        Args:
            socio_id: ID del socio
            socio_nombre: Nombre del socio (opcional)
        """
        self.id = str(uuid.uuid4())
        self.socio_id = socio_id
        self.socio_nombre = socio_nombre or f"Socio({socio_id[:8]})"
        ahora = datetime.now()
        self.fecha = ahora.date()
        self.hora = ahora.time()

    def registrar_acceso(self) -> str:
        """Retorna un mensaje de confirmación del acceso."""
        return f"Acceso registrado para {self.socio_nombre} el {self.fecha} a las {self.hora.strftime('%H:%M:%S')}"

    def __str__(self):
        return (f"Acceso(id={self.id[:8]}, socio={self.socio_nombre:<20}, "
                f"fecha={self.fecha}, hora={self.hora.strftime('%H:%M:%S')})")