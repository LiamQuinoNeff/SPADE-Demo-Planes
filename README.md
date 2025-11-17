**Overview**

Esta carpeta contiene una pequeña simulación de control de tráfico aéreo usando agentes SPADE (Python), adaptado de un ejemplo en JADE (Java).

**Files**
- `hostAgent.py`: entrypoint — crea y arranca la `Torre` y N `Avion` agents.
- `torreAgent.py`: agente Torre, maneja la pista y responde a mensajes de los aviones.
- `avionAgent.py`: agente Avión, envía informes periódicos y solicita permiso para aterrizar.

**Flujo / Lógica (resumen)**
- El `HostAgent` arranca `TorreAgent` (JID `torre@localhost`) y N `AvionAgent` (ej. `avion0@localhost`, `avion1@localhost`, ...).
- Cada `AvionAgent` tiene 3 comportamientos principales:
  - `StatusTick` (cada 1s): imprime estado (depuración).
  - `SendVolando` (cada 5s): envía a la torre un mensaje con `body = "volando"` (`performative: inform`).
  - `RequestLanding` (cada 10s): envía `body = "aterrizar"` (`performative: propose`).
  - `RecvBehav`: recibe respuestas de la torre. Si la torre responde `aceptar`, el avión inicia `LandingBehav`.
  - `LandingBehav`: simula el aterrizaje (espera 2s), envía `body = "liberar"` a la torre y finaliza su agente.
- `TorreAgent` procesa mensajes y mantiene una bandera `pista_ocupada`:
  - Si recibe `volando` responde `recibido`.
  - Si recibe `aterrizar` y la pista está libre: responde `aceptar` y marca `pista_ocupada=True`.
  - Si recibe `aterrizar` y la pista está ocupada: responde `rechazo`.
  - Si recibe `liberar` o `fin`: marca la pista como libre y responde `liberado`.

**Cómo ejecutar (requisitos mínimos)**
- Requisitos:
  - Python 3.8+ con virtualenv y la biblioteca `spade` instalada dentro del entorno.
  - Un servidor XMPP accesible (local o remoto). SPADE necesita cuentas XMPP para los JIDs usados.

- Ejecutar (desde la carpeta `./aviones`):
```powershell
# activar tu entorno virtual (ejemplo en Windows PowerShell)
& C:/SPADE/cst/Scripts/Activate.ps1

# ejecutar el host (crea torre y aviones)
py hostAgent.py
```

**Consejos y mejoras posibles**
- Manejar `pista_ocupada` con más cuidado si se escala la simulación (locks o colas internas).
- Reducir ruido por consola/eliminar `StatusTick` si se desea menos salida.

**Estado actual del código**
- Se corrigieron errores detectados inicialmente:
  - No await en `add_behaviour()` (no es awaitable).
  - La `Torre` ya no se detiene tras procesar un solo mensaje.
- La simulación básica funciona: la torre concede permiso a un avión a la vez; éste aterriza y libera la pista; otros aviones reciben rechazo hasta que la pista se libera.

