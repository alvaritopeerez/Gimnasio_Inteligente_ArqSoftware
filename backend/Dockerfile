FROM python:3.12-slim

WORKDIR /app

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY src/ ./src/

# Exponer el puerto
EXPOSE 8000

# Ejecutar la aplicación
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]