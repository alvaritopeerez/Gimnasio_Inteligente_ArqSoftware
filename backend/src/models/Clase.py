import uuid
from datetime import datetime
from typing import List

class Clase:
    def __init__(self, nombre: str, horario: str, aforo: int, entrenador_id: str):
        if not nombre.strip():
            raise ValueError("Error: el nombre no puede estar vacío.")
        try:
            datetime.strptime(horario, "%H:%M")
        except ValueError:
            raise ValueError("Error: horario inválido. Use formato HH:MM")
        if aforo <= 0:
            raise ValueError("Error: el aforo debe ser positivo.")

        self.id = str(uuid.uuid4())
        self.nombre = nombre
        self.horario = horario
        self.aforo = aforo
        self.entrenador_id = entrenador_id
        self.socios_inscritos: List[str] = []

    def verificar_disponibilidad(self) -> bool:
        return len(self.socios_inscritos) < self.aforo

    def inscribir_socio(self, socio_id: str) -> bool:
        if socio_id in self.socios_inscritos:
            return False
        if not self.verificar_disponibilidad():
            raise ValueError("Error: la clase está completa.")
        self.socios_inscritos.append(socio_id)
        return True

    def cancelar_reserva(self, socio_id: str) -> bool:
        if socio_id in self.socios_inscritos:
            self.socios_inscritos.remove(socio_id)
            return True
        return False

    def plazas_disponibles(self) -> int:
        return self.aforo - len(self.socios_inscritos)