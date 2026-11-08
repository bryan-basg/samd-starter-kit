# Dockerfile — imagen mínima del backend del esqueleto de ejemplo (FastAPI).
# Úsala con docker-compose.yml (servicio `backend`) o para un build standalone.
#
# SaMD (IEC 62304 §8, SOUP): la imagen base va pineada por DIGEST (@sha256:...), no
# solo por etiqueta. `3.12-slim` es una etiqueta mutable: su dueño la reapunta a otra
# imagen y el próximo build sale distinto sin que cambie el diff — ni reproducible ni
# auditable. La etiqueta queda al lado para que se lea qué versión es; manda el digest
# (el del índice multi-arquitectura). Dependabot (`docker` en `.github/dependabot.yml`)
# propone el digest nuevo cuando la etiqueta avanza. Guardián:
# `tests/test_workflows_pineados_a_sha.py::test_toda_imagen_de_contenedor_esta_pineada_a_digest`.
FROM python:3.12-slim@sha256:4840d514c583a4d3d8cad3940e68dee6f0f6f3635c12fcd0a3d74c21a5b93a54

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
