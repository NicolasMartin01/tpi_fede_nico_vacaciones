import os

CARPETA_DATOS = os.path.join(os.path.dirname(__file__), "datos")
ARCHIVO_EMPLEADOS = os.path.join(CARPETA_DATOS, "empleados.csv")
ARCHIVO_SOLICITUDES = os.path.join(CARPETA_DATOS, "solicitudes.csv")

ENCABEZADO_EMPLEADOS = ["legajo", "nombre", "dias_disponibles", "contrasena"]
ENCABEZADO_SOLICITUDES = [
    "id",
    "legajo",
    "nombre",
    "dias",
    "estado",
    "observacion",
]

EMPLEADOS_INICIALES = [
    ["1001", "Federico Moretto", "14", "fede123"],
    ["1002", "Nicolas Martin", "5", "nico456"],
    ["1003", "Lucia Gomez", "20", "lucia789"],
]

ESTADO_PENDIENTE = "PENDIENTE"
ESTADO_APROBADA = "APROBADA"
ESTADO_RECHAZADA_SALDO = "RECHAZADA_SALDO"
ESTADO_RECHAZADA_SUPERVISOR = "RECHAZADA_SUPERVISOR"
ESTADO_EMPLEADO_INEXISTENTE = "EMPLEADO_INEXISTENTE"

# Telegram conversation states
PEDIR_LEGAJO, PEDIR_CONTRASENA, PEDIR_DIAS = range(3)
