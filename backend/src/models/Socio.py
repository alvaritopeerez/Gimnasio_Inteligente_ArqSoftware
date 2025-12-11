import uuid
import re
from datetime import date
from typing import List
from passlib.context import CryptContext  # NUEVO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # NUEVO
fecha_nacimiento = "2005-03-15"


class Usuario:
    def __init__(self, nombre: str, email: str):
        if not nombre.strip():
            raise ValueError("Error: el nombre no puede estar vacío.")

        email_pattern = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(email_pattern, email):
            raise ValueError("Error: email inválido.")

        self.id = str(uuid.uuid4())
        self.nombre = nombre
        self.email = email


class Socio(Usuario):
    def __init__(
        self,
        nombre: str,
        email: str,
        fecha_nacimiento: str,
        nivel: str = "principiante",
        password: str = "",
    ):
        super().__init__(nombre, email)

        try:
            fecha_obj = date.fromisoformat(fecha_nacimiento)
            if fecha_obj > date.today():
                raise ValueError("La fecha de nacimiento no puede ser futura.")
        except ValueError as e:
            if "Invalid isoformat" in str(e):
                raise ValueError(f"Formato inválido. Usa YYYY-MM-DD: {fecha_nacimiento}")
            else:
                raise ValueError(f"Error en fecha de nacimiento: {e}")

        niveles_validos = ["principiante", "intermedio", "avanzado"]
        if nivel.lower() not in niveles_validos:
            raise ValueError(f"Nivel inválido. Debe ser: {', '.join(niveles_validos)}")

        self.fecha_nacimiento = fecha_nacimiento
        self.nivel = nivel.lower()

        # Guardar hash, no la contraseña en claro
        self.password_hash = pwd_context.hash(password) if password else ""

        self.clases_reservadas: List[str] = []
        self.rutinas: List[str] = []
        self.progresos: List[str] = []

    def verificar_contrasena(self, password: str) -> bool:
        if not self.password_hash:
            return False
        return pwd_context.verify(password, self.password_hash)

    def reservar_clase(self, clase_id: str) -> None:
        if clase_id not in self.clases_reservadas:
            self.clases_reservadas.append(clase_id)

    def cancelar_reserva(self, clase_id: str) -> None:
        if clase_id in self.clases_reservadas:
            self.clases_reservadas.remove(clase_id)

    def asignar_rutina(self, rutina_id: str) -> None:
        if rutina_id not in self.rutinas:
            self.rutinas.append(rutina_id)

    def registrar_progreso(self, progreso_id: str) -> None:
        self.progresos.append(progreso_id)