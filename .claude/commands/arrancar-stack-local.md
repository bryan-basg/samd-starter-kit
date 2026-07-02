---
description: Levanta el stack local completo (emuladores/servicios de {{CLOUD_STACK}} + backend {{BACKEND_STACK}} + frontend {{FRONTEND_STACK}}) y siembra usuarios canónicos con login funcional.
---

Sos un asistente que arranca el entorno de desarrollo local de {{PROJECT_NAME}}. Ejecutá los pasos EN ORDEN. El objetivo es tener el stack corriendo con login funcional sin atorones, tal como quedó validado la última vez que alguien del equipo lo levantó desde cero.

## Pasos (en este orden exacto)

```bash
# 1. Emuladores/servicios locales de auth + datos (ej. Firebase emulators, LocalStack, docker-compose de {{DB_STACK}})
cd <ruta del repo>
<comando de arranque de emuladores de {{CLOUD_STACK}}> &

# 2. Backend {{BACKEND_STACK}} con las env vars críticas del entorno local
<VAR_CRITICA_1>=<valor> \
  <VAR_CRITICA_2>=<valor> \
  <comando de arranque del backend, ej. uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload> &

# 3. Frontend {{FRONTEND_STACK}}
cd frontend && npm run dev &

# 4. Sembrar / sincronizar usuarios BD <-> emulador de auth (password unificada de dev)
python3 scripts/maintenance/<script_de_reset_de_usuarios>.py
```

Si el backend tira `ModuleNotFoundError` engañoso al correr tests o levantar el server, activá primero el entorno virtual/gestor de dependencias del proyecto (síntoma clásico de correr el intérprete global en vez del del venv/entorno del repo).

## Por qué cada env var (no las omitas)

- **Flag de "saltar migraciones" en local** (ej. `SKIP_MIGRATIONS=true`): si el árbol de migraciones local tiene heads paralelos sin mergear, o simplemente no querés que el arranque local dispare migraciones contra tu BD de desarrollo, el backend puede quedar atorado en el startup esperando resolver ese estado. Documentá cualquier deuda de este tipo como pendiente explícito en vez de dejar que sea "magia" que alguien tiene que redescubrir.
- **Host del emulador de autenticación** (ej. `FIREBASE_AUTH_EMULATOR_HOST=127.0.0.1:9111` o el equivalente de tu proveedor de auth): sin este flag, el backend valida los tokens contra el servicio de auth real y rechaza los tokens emitidos por el emulador local (porque llevan un algoritmo/firma distinta). La rama de código que acepta tokens de emulador normalmente ya existe en el servicio de verificación de auth — lo que falta es setear la variable, no escribir código nuevo.
- **Password unificada de desarrollo**: el script de reset/siembra de usuarios debería borrar del emulador los usuarios que no estén en la lista canónica y recrear los de referencia con una password fija conocida. Sin correrlo, el alta de usuario puede fallar en silencio (ej. "el email ya existe") y dejar passwords viejas de una corrida anterior, lo que se disfraza de "el login no funciona" cuando en realidad es un dato sembrado obsoleto.

## Usuarios canónicos de referencia

Definí en el repo (no en la cabeza de cada dev) una tabla de usuarios de prueba con rol y propósito — típicamente al menos: una cuenta admin/dueño del proyecto, una cuenta de usuario final típico, y una cuenta por cada rol adicional relevante al dominio (ej. un rol profesional/operador si el producto lo tiene). Todas con la misma password de desarrollo para no tener que recordar credenciales distintas.

Nota: los emails/dominios exactos son los que defina el script de siembra del repo (fuente de verdad) — no los inventes ni los copies de otro proyecto.

## Trampa a vigilar: variables de entorno de testing que fuerzan estados especiales

Si el frontend tiene una variable de entorno (gitignored, ej. `VITE_ONBOARDING_TESTER_EMAIL` o similar) que fuerza un comportamiento especial para "cuentas de tester" (por ejemplo, repetir el onboarding en cada login para poder grabarlo de nuevo), tené cuidado de no meter ahí la cuenta que usás como tu login habitual de trabajo diario — vas a terminar viendo ese comportamiento especial todo el tiempo y vas a perder horas pensando que es un bug de lógica de negocio cuando es simplemente esa variable. Si reaparece un síntoma tipo "el onboarding/flujo especial sale aunque la BD diga que ya se completó", revisá primero esa variable antes de tocar código.

Al terminar, reportá qué procesos quedaron corriendo y en qué puertos (emuladores, backend, frontend). No dejes procesos de desarrollo colgados sin avisar.
