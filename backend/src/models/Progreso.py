import uuid
from datetime import datetime
from typing import Optional

class Progreso:
    """Registro de progreso físico de un socio."""

    def __init__(self, socio_id: str, peso: float, repeticiones: int, tiempo: int):
        """
        Inicializa un registro de progreso.

        Args:
            socio_id: ID del socio
            peso: Peso levantado en kg (0 si no aplica)
            repeticiones: Número de repeticiones realizadas
            tiempo: Tiempo de ejercicio en segundos
        """
        if peso < 0:
            raise ValueError("Error: el peso no puede ser negativo.")

        if repeticiones < 0:
            raise ValueError("Error: las repeticiones no pueden ser negativas.")

        if tiempo < 0:
            raise ValueError("Error: el tiempo no puede ser negativo.")

        self.id = str(uuid.uuid4())
        self.socio_id = socio_id
        self.fecha = datetime.now()
        self.peso = peso
        self.repeticiones = repeticiones
        self.tiempo = tiempo  # en segundos

    def registrar(self) -> str:
        """Retorna un mensaje de confirmación del registro."""
        return f"Progreso registrado: {self.peso}kg, {self.repeticiones} reps, {self.tiempo}s"

    def __str__(self):
        fecha_str = self.fecha.strftime("%Y-%m-%d %H:%M")
        return (f"Progreso(id={self.id[:8]}, fecha={fecha_str}, "
                f"peso={self.peso}kg, reps={self.repeticiones}, tiempo={self.tiempo}s)")
