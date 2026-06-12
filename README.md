# Chatbot de Vacaciones — Telegram

Bot de Telegram para gestión de solicitudes de vacaciones. El empleado interactúa con el bot y el supervisor recibe la solicitud con botones para aprobar o rechazar.

## Requisitos previos

- Python 3.10 o superior
- Cuenta de Telegram
- Un bot creado en [@BotFather](https://t.me/BotFather)

## Instalación

Cloná el repositorio e instalá las dependencias:

```bash
git clone https://github.com/NicolasMartin01/tpi_fede_nico_vacaciones.git
cd tpi_fede_nico_vacaciones
pip install -r requirements.txt
```

## Configuración

### 1. Crear el archivo .env

Copiá el archivo de ejemplo:

```bash
# Linux / macOS
cp .env.example .env

# Windows
copy .env.example .env
```

### 2. Completar las variables de entorno

Editá el archivo `.env` con tus valores:

```
BOT_TOKEN=123456789:AAFxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SUPERVISOR_CHAT_ID=987654321
```

#### Cómo obtener el BOT_TOKEN

1. Abrí Telegram y buscá **@BotFather**.
2. Enviá `/newbot` y seguí las instrucciones.
3. BotFather te va a entregar un token — ese es tu `BOT_TOKEN`.

#### Cómo obtener el SUPERVISOR_CHAT_ID

**Chat personal:** buscá **@userinfobot** en Telegram y enviále cualquier mensaje. Te responde con tu ID numérico.

**Grupo:** agregá el bot al grupo, enviá un mensaje y abrí en el navegador:
```
https://api.telegram.org/bot<BOT_TOKEN>/getUpdates
```
Buscá `"chat": {"id": ...}` en la respuesta. Los IDs de grupo son negativos (ej: `-1001234567890`).

## Ejecutar el bot

```bash
python main.py
```

El bot queda corriendo. Para detenerlo usá `Ctrl+C`.

## Uso

1. El empleado inicia la conversación con `/start`.
2. El bot pide el legajo y la contraseña.
3. El bot muestra los días disponibles y pide la cantidad a solicitar.
4. Si hay saldo suficiente, la solicitud queda en estado `PENDIENTE` y se notifica al supervisor.
5. El supervisor recibe el mensaje con botones **Aprobar** / **Rechazar**.
6. El empleado recibe la respuesta final.

Para cancelar en cualquier momento: `/cancelar`.

## Datos de prueba

| Legajo | Nombre           | Contraseña | Días disponibles |
|--------|------------------|------------|-----------------|
| 1001   | Federico Moretto | fede123    | 14              |
| 1002   | Nicolas Martin   | nico456    | 5               |
| 1003   | Lucia Gomez      | lucia789   | 20              |

Para resetear los datos, eliminá `datos/empleados.csv` y `datos/solicitudes.csv`. Se regeneran al iniciar el bot.
