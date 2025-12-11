# Sistema de Gestión de Gimnasio Inteligente

> **Proyecto Final de Arquitectura de Software**
> Una solución integral basada en microservicios para la gestión de centros deportivos, entrenamiento personalizado e integración IoT.

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)

---

## Descripción del Proyecto

Este proyecto implementa una arquitectura de software moderna y escalable para la administración de un gimnasio. Ha sido diseñado siguiendo una **Arquitectura de Microservicios contenerizada** que desacopla la lógica de negocio (Backend) de la interfaz de usuario (Frontend), cumpliendo al 100% con los artefactos de diseño UML.

---

## Arquitectura Técnica

El proyecto se despliega mediante Docker Compose en dos servicios principales:

### Backend (API RESTful)
* **Framework:** FastAPI.
* **Patrón de Diseño:** Arquitectura en Capas (Controller -> Service -> Modelos).
* **Seguridad:** Autenticación **OAuth2** con tokens **JWT** y hashing de contraseñas con Bcrypt.
* **Inicialización (`Lifespan`):** Implementación de **Data Seeding** (`startup_event`) para crear automáticamente Entrenadores, Clases, Rutinas y el dispositivo de prueba (`pulsera-web`) al iniciar el sistema.

### Frontend (Interfaz de Usuario)
* **Framework:** Streamlit.
* **Fluidez y UX:** Uso extensivo de **Callbacks** (`on_click`) para garantizar que todas las acciones (reservar, asignar, simular IoT) se ejecuten y actualicen la interfaz en **un solo clic**, evitando el doble-click de recarga.

---

## Funcionalidades Principales

1.  **Gestión de Usuario:**
    * Registro y Login de Socio.
    * Perfil detallado con fecha de nacimiento visible.
2.  **Clases y Reservas:**
    * Reserva y Cancelación de clases con control de aforo estricto en el Backend.
3.  **Entrenamiento:**
    * Asignación de rutinas (auto-asignación desde el catálogo).
    * Pestaña "Mis Rutinas" para ver el plan asignado.
4.  **Integración IoT & Progreso:**
    * Simulador de actividad integrado en el Frontend.
    * El Backend implementa el flujo de **Sincronización** (`sincronizarDatos`) y **Registro de Progreso** (`registrarProgreso`) conforme al diagrama de secuencia.
5.  **Control de Acceso:**
    * Simulación de registro de entrada/salida (Torno QR) desde el perfil.

---

## Instalación y Ejecución

El despliegue es inmediato gracias a Docker.

### Prerrequisitos
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y ejecutándose.

### Pasos para ejecutar

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/alvaritopeerez/Gimnasio_Inteligente_ArqSoftware.git](https://github.com/alvaritopeerez/Gimnasio_Inteligente_ArqSoftware.git)
    cd PROYECTO_GIMNASIO
    ```

2.  **Construir y levantar los servicios (Necesario después de cualquier cambio de código):**
    ```bash
    docker-compose up --build
    ```

3.  **Acceder a la aplicación:**

    * **Frontend (Web App):** [http://localhost:8501](http://localhost:8501)
    
    * **Backend (Documentación Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
        * *(Usar para probar la API directamente y gestionar Entrenadores/Rutinas).*

---

## Estructura del Proyecto

```text
PROYECTO_GIMNASIO/
├── docker-compose.yml          # Orquestador de servicios
├── backend/                    # Microservicio de API
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src/
│       ├── main.py             # Entrypoint & Endpoints (Controller)
│       ├── auth.py             # Lógica de Seguridad (JWT)
│       ├── Services/           # Lógica de Negocio
│       ├── models/             # Entidades del Dominio (Socio, Clase, etc.)
│       └── schemas/            # DTOs para validación de datos
└── frontend/                   # Microservicio de UI
    ├── Dockerfile
    ├── requirements.txt
    └── app.py                  # Aplicación Streamlit

---
## Autor

* **Álvaro Pérez**

## Colaboradores

* **Juan Faginas, Fernando Galán**

---
*Proyecto desarrollado para la asignatura de Arquitectura del Software - [Semestre 5].*