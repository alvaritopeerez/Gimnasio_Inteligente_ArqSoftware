import uuid
from typing import List, Dict, Any

class Rutina:
    """Rutina de ejercicios que puede ser asignada a socios."""

    def __init__(self, nombre: str, duracion: int, dificultad: str):
        """
        Inicializa una rutina.

        Args:
            nombre: Nombre de la rutina (ej: "Fuerza Superior", "Cardio Intenso")
            duracion: Duración en minutos
            dificultad: Nivel (principiante, intermedio, avanzado)
        """
        if not nombre.strip():
            raise ValueError("Error: el nombre no puede estar vacío.")

        if duracion <= 0:
            raise ValueError("Error: la duración debe ser positiva.")

        dificultades_validas = ["principiante", "intermedio", "avanzado"]
        if dificultad.lower() not in dificultades_validas:
            raise ValueError(f"Error: dificultad inválida. Debe ser: {', '.join(dificultades_validas)}")

        self.id = str(uuid.uuid4())
        self.nombre = nombre
        self.duracion = duracion
        self.dificultad = dificultad.lower()
        self.ejercicios: List[Dict[str, Any]] = []  # Lista de ejercicios

    def anadir_ejercicio(self, nombre_ejercicio: str, repeticiones: int = 10, series: int = 3) -> None:
        """
        Añade un ejercicio a la rutina.

        Args:
            nombre_ejercicio: Nombre del ejercicio
            repeticiones: Número de repeticiones por serie
            series: Número de series
        """
        if not nombre_ejercicio.strip():
            raise ValueError("Error: el nombre del ejercicio no puede estar vacío.")

        if repeticiones <= 0 or series <= 0:
            raise ValueError("Error: repeticiones y series deben ser positivas.")

        ejercicio = {
            "nombre": nombre_ejercicio,
            "repeticiones": repeticiones,
            "series": series
        }
        self.ejercicios.append(ejercicio)

    def get_ejercicios(self) -> List[Dict[str, Any]]:
        """Retorna la lista de ejercicios."""
        return self.ejercicios.copy()

    def __str__(self):
        return (f"Rutina(id={self.id[:8]}, nombre={self.nombre:<25}, "
                f"duración={self.duracion}min, dificultad={self.dificultad:<12}, "
                f"ejercicios={len(self.ejercicios)})")