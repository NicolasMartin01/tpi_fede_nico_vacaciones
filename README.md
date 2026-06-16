# Chatbot de Vacaciones — Telegram

Proyecto desarrollado para el Trabajo Practico Integrador de Organizacion Empresarial.

La solucion automatiza el proceso de solicitud de vacaciones mediante un chatbot de Telegram, permitiendo validar empleados, registrar solicitudes y gestionar la aprobacion o rechazo por parte de un supervisor.

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

## Flujo de la aplicación

El bot implementa el proceso de gestión de vacaciones con dos actores: el **empleado** y el **supervisor**.

### Lado del empleado

1. El empleado inicia la conversación enviando `/start`.
2. El bot solicita el **legajo**. Si no existe en el sistema, registra el intento como `EMPLEADO_INEXISTENTE` y finaliza.
3. El bot solicita la **contraseña**. Si es incorrecta, cancela la operación.
4. El bot muestra el nombre del empleado y sus **días disponibles**, y pide la cantidad de días a solicitar.
5. Si los días solicitados superan el saldo disponible, la solicitud se registra como `RECHAZADA_SALDO` y finaliza.
6. Si hay saldo suficiente, la solicitud se guarda como `PENDIENTE` y el empleado recibe confirmación de que está a la espera de aprobación.

### Lado del supervisor

7. El supervisor recibe un mensaje en su chat con los datos de la solicitud (ID, nombre, legajo, días) y dos botones: **✅ Aprobar** y **❌ Rechazar**.
8. Si aprueba: los días se descuentan del saldo del empleado, la solicitud pasa a `APROBADA` y el empleado recibe una notificación de aprobación.
9. Si rechaza: la solicitud pasa a `RECHAZADA_SUPERVISOR` y el empleado recibe una notificación de rechazo.

### Estados posibles de una solicitud

| Estado                  | Descripción                                      |
|-------------------------|--------------------------------------------------|
| `PENDIENTE`             | Enviada al supervisor, esperando respuesta       |
| `APROBADA`              | Aprobada por el supervisor                       |
| `RECHAZADA_SUPERVISOR`  | Rechazada por el supervisor                      |
| `RECHAZADA_SALDO`       | Rechazada automáticamente por saldo insuficiente |
| `EMPLEADO_INEXISTENTE`  | El legajo ingresado no existe en el sistema      |

Para cancelar en cualquier momento: `/cancelar`.

## Datos de prueba

| Legajo | Nombre           | Contraseña | Días disponibles |
|--------|------------------|------------|-----------------|
| 1001   | Federico Moretto | fede123    | 14              |
| 1002   | Nicolas Martin   | nico456    | 5               |
| 1003   | Lucia Gomez      | lucia789   | 20              |

Para resetear los datos, eliminá `datos/empleados.csv` y `datos/solicitudes.csv`. Se regeneran al iniciar el bot.

## Capturas de pantalla

En la carpeta assets se encuentran las capturas de pantalla de las interacciones realizadas con ChatGPT utilizadas durante el desarrollo del trabajo. Se incluyen por separado para evitar aumentar el tamaño del documento principal.