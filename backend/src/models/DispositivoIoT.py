import uuid
import random
from datetime import datetime
from typing import Dict, Any

class DispositivoIoT:
    """Dispositivo IoT que recopila datos biométricos de socios."""

    def __init__(self, tipo: str, socio_id: str):
        """
        Inicializa un dispositivo IoT.

        Args:
            tipo: Tipo de dispositivo (pulsera, báscula, sensor)
            socio_id: ID del socio propietario
        """
        tipos_validos = ["pulsera", "bascula", "sensor"]
        if tipo.lower() not in tipos_validos:
            raise ValueError(f"Error: tipo inválido. Debe ser: {', '.join(tipos_validos)}")

        self.id = str(uuid.uuid4())
        self.tipo = tipo.lower()
        self.socio_id = socio_id
        self.datos: Dict[str, Any] = {}

    def recopilar_datos(self) -> Dict[str, Any]:
        """
        Simula la recopilación de datos biométricos.

        Returns:
            Diccionario con datos simulados según el tipo de dispositivo
        """
        if self.tipo == "pulsera":
            self.datos = {
                "pulsaciones": random.randint(60, 120),
                "pasos": random.randint(1000, 15000),
                "calorias": round(random.uniform(50, 300), 2),
                "peso_levantado": round(random.uniform(1.0, 5.0), 1),
                "repeticiones": random.randint(1, 5),
                "tiempo_ejercicio": random.randint(300, 1800),
                "timestamp": datetime.now().isoformat()
            }
        elif self.tipo == "bascula":
            self.datos = {
                "peso": round(random.uniform(50, 100), 1),
                "grasa_corporal": round(random.uniform(10, 30), 1),
                "masa_muscular": round(random.uniform(30, 50), 1),
                "timestamp": datetime.now().isoformat()
            }
        elif self.tipo == "sensor":
            self.datos = {
                "repeticiones": random.randint(5, 20),
                "peso_levantado": round(random.uniform(10, 50), 1),
                "tiempo_ejercicio": random.randint(30, 300),
                "timestamp": datetime.now().isoformat()
            }

        return self.datos

    def sincronizar(self) -> bool:
        """
        Simula la sincronización de datos con el sistema.

        Returns:
            True si la sincronización fue exitosa
        """
        if not self.datos:
            self.recopilar_datos()
        return True

    def __str__(self):
        return (f"DispositivoIoT(id={self.id[:8]}, tipo={self.tipo:<10}, "
                f"socio_id={self.socio_id[:8]}, datos={'Sí' if self.datos else 'No'})")