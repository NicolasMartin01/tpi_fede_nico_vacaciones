# Chatbot de Vacaciones — Telegram

Proyecto desarrollado para el Trabajo Practico Integrador de Organizacion Empresarial.

La solucion automatiza el proceso de solicitud de vacaciones mediante un chatbot de Telegram, permitiendo validar empleados, registrar solicitudes y gestionar la aprobacion o rechazo por parte de un supervisor.

## Requisitos previos

- Python 3.10 o superior **— o Docker** (ver sección [Ejecutar con Docker](#ejecutar-con-docker))
- Cuenta de Telegram
- Un bot creado en [@BotFather](https://t.me/BotFather)

## Instalación

Cloná el repositorio (igual en todas las plataformas):

```bash
git clone https://github.com/NicolasMartin01/tpi_fede_nico_vacaciones.git
cd tpi_fede_nico_vacaciones
```

Instalá las dependencias:

**Linux / macOS**:
```bash
pip3 install -r requirements.txt
```

**Windows**:
```cmd
pip install -r requirements.txt
```

> En Windows, Python se instala como `python` / `pip`. En Linux y macOS coexisten con Python 2, por eso se usa `python3` / `pip3`.

## Configuración

### 1. Crear el archivo .env

**Linux / macOS**:
```bash
cp .env.example .env
```

**Windows — CMD**:
```cmd
copy .env.example .env
```

**Windows — PowerShell**:
```powershell
Copy-Item .env.example .env
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

**Linux / macOS**:
```bash
python3 main.py
```

**Windows**:
```cmd
python main.py
```

El bot queda corriendo. Para detenerlo usá `Ctrl+C`.

## Ejecutar con Docker

Esta opción no requiere tener Python instalado en la máquina.

### 1. Construir la imagen

El comando es igual en todas las plataformas:

```bash
docker build -t bot-vacaciones .
```

### 2. Ejecutar el contenedor

La única diferencia entre plataformas está en cómo se escribe la ruta del volumen (`-v`).

**Linux / macOS** (Terminal):
```bash
docker run --env-file .env -v ./datos:/app/datos bot-vacaciones
```

**Windows — PowerShell**:
```powershell
docker run --env-file .env -v ${PWD}/datos:/app/datos bot-vacaciones
```

**Windows — CMD**:
```cmd
docker run --env-file .env -v %cd%/datos:/app/datos bot-vacaciones
```

- `--env-file .env` — inyecta las variables de entorno sin incluirlas en la imagen.
- `-v <ruta>/datos:/app/datos` — monta la carpeta `datos/` como volumen para que los CSVs persistan entre reinicios.

### 3. Ejecutar en segundo plano (opcional)

**Linux / macOS**:
```bash
docker run -d --name bot-vacaciones --env-file .env -v ./datos:/app/datos bot-vacaciones
```

**Windows — PowerShell**:
```powershell
docker run -d --name bot-vacaciones --env-file .env -v ${PWD}/datos:/app/datos bot-vacaciones
```

**Windows — CMD**:
```cmd
docker run -d --name bot-vacaciones --env-file .env -v %cd%/datos:/app/datos bot-vacaciones
```

El flag `-d` ejecuta el contenedor en segundo plano (no bloquea la terminal).

Para ver los logs (igual en todas las plataformas):
```bash
docker logs -f bot-vacaciones
```

Para detenerlo (igual en todas las plataformas):
```bash
docker stop bot-vacaciones
```

> **Nota:** si cambiás el `.env`, no es necesario reconstruir la imagen. Alcanza con detener el contenedor y volver a ejecutarlo.

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