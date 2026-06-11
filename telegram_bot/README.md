# Chatbot de Vacaciones — Telegram

Versión Telegram del simulador de gestión de vacaciones. El empleado interactúa con el bot, y el supervisor recibe la solicitud en un chat separado con botones para aprobar o rechazar.

## Requisitos

- Python 3.10 o superior
- Cuenta de Telegram
- Acceso a [@BotFather](https://t.me/BotFather) para crear el bot

## Instalación

```bash
cd telegram_bot
pip install -r requirements.txt
```

## Configuración

### 1. Obtener el BOT_TOKEN

1. Abrí Telegram y buscá **@BotFather**.
2. Enviá el comando `/newbot`.
3. Seguí las instrucciones: elegí un nombre y un username para el bot (debe terminar en `bot`, ej: `vacaciones_tpi_bot`).
4. BotFather te va a responder con un token con este formato:
   ```
   123456789:AAFxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
5. Copiá ese token, ese es tu `BOT_TOKEN`.

### 2. Obtener el SUPERVISOR_CHAT_ID

El `SUPERVISOR_CHAT_ID` es el ID numérico del chat (personal o grupo) donde el supervisor va a recibir las solicitudes.

**Para un chat personal:**
1. Buscá **@userinfobot** en Telegram.
2. Enviále cualquier mensaje.
3. Te va a responder con tu ID numérico (ej: `987654321`).

**Para un grupo:**
1. Agregá el bot al grupo.
2. Enviá cualquier mensaje en el grupo.
3. Abrí en el navegador:
   ```
   https://api.telegram.org/bot<BOT_TOKEN>/getUpdates
   ```
4. En la respuesta JSON buscá `"chat": {"id": ...}` dentro del mensaje del grupo. El ID de grupos es negativo (ej: `-1001234567890`).

### 3. Crear el archivo .env

Copiá el archivo de ejemplo y completá los valores:

```bash
cp .env.example .env
```

Editá `.env`:

```
BOT_TOKEN=123456789:AAFxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SUPERVISOR_CHAT_ID=987654321
```

## Ejecutar el bot

```bash
cd telegram_bot
python main.py
```

El bot queda corriendo. Para detenerlo usá `Ctrl+C`.

## Flujo del bot

1. El empleado inicia la conversación con `/start`.
2. El bot pide el legajo y valida que exista.
3. El bot muestra los días disponibles y pide la cantidad a solicitar.
4. Si hay saldo suficiente, la solicitud queda en estado `PENDIENTE` y se notifica al supervisor.
5. El supervisor recibe el mensaje con botones **Aprobar** / **Rechazar**.
6. El empleado recibe la respuesta final del supervisor.

Para cancelar en cualquier momento: `/cancelar`.

## Datos de prueba

Los empleados de ejemplo cargados al iniciar son:

| Legajo | Nombre           | Días disponibles |
|--------|------------------|-----------------|
| 1001   | Federico Moretto | 14              |
| 1002   | Nicolas Martin   | 5               |
| 1003   | Lucia Gomez      | 20              |

Para resetear los datos, eliminá los archivos `datos/empleados.csv` y `datos/solicitudes.csv`. Se van a regenerar al iniciar el bot.
