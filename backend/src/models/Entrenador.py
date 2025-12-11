import uuid
import re
from typing import List

class Entrenador:
    def __init__(self, nombre: str, email: str, especialidad: str):
        if not nombre.strip():
            raise ValueError("Error: el nombre no puede estar vacío.")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Error: email inválido.")
        if not especialidad.strip():
            raise ValueError("Error: la especialidad no puede estar vacía.")

        self.id = str(uuid.uuid4())
        self.nombre = nombre
        self.email = email
        self.especialidad = especialidad
        self.clases_impartidas: List[str] = []

    def crear_clase(self, clase_id: str) -> None:
        if clase_id not in self.clases_impartidas:
            self.clases_impartidas.append(clase_id)