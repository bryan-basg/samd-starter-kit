# Dockerfile — imagen mínima del backend del esqueleto de ejemplo (FastAPI).
# Úsala con docker-compose.yml (servicio `backend`) o para un build standalone.
#
# SaMD: en PRODUCCIÓN, pineá la imagen del deploy por digest (@sha256:...), nunca por
# tag mutable como :latest — evita rollbacks ciegos ante un incidente. Acá usamos un
# tag legible porque es solo el entorno de desarrollo local.
FROM python:3.12-slim

# No escribir .pyc y flush inmediato de logs (mejor diagnóstico en contenedor).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Capa de deps primero para aprovechar el cache de Docker.
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

# Código de la app (en compose se monta como volumen encima para hot-reload).
COPY app/ ./app/

# Usuario no-root (Trivy DS-0002, severidad HIGH). Un contenedor que corre como root
# convierte cualquier ejecución remota de código en un escape de contenedor con
# privilegios totales — inaceptable en un dispositivo que procesa datos de salud
# (ISO 14971 + GDPR Art. 32 / HIPAA Security Rule). Se crea el usuario y se le da
# la propiedad de /app para que uvicorn pueda leer el código.
RUN useradd --create-home --uid 10001 appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# --reload para desarrollo; en prod usá un comando sin reload y con varios workers.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
