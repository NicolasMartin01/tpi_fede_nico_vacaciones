import csv
import os
from datetime import datetime, timedelta


CARPETA_DATOS = "datos"
ARCHIVO_EMPLEADOS = os.path.join(CARPETA_DATOS, "empleados.csv")
ARCHIVO_SOLICITUDES = os.path.join(CARPETA_DATOS, "solicitudes.csv")

FORMATO_FECHA = "%d/%m/%Y"

ENCABEZADO_EMPLEADOS = ["legajo", "nombre", "dias_disponibles"]
ENCABEZADO_SOLICITUDES = [
    "id",
    "legajo",
    "nombre",
    "dias_solicitados",
    "fecha_inicio",
    "fecha_fin",
    "estado",
    "observacion",
]

EMPLEADOS_INICIALES = [
    ["1001", "Federico Moretto", "14"],
    ["1002", "Juan Perez", "5"],
    ["1003", "Lucia Gomez", "20"],
]

ESTADO_APROBADA = "APROBADA"
ESTADO_PENDIENTE = "PENDIENTE_SUPERVISOR"
ESTADO_RECHAZADA_SALDO = "RECHAZADA_SALDO_INSUFICIENTE"
ESTADO_RECHAZADA_SUPERVISOR = "RECHAZADA_SUPERVISOR"
ESTADO_EMPLEADO_INEXISTENTE = "EMPLEADO_INEXISTENTE"


def crear_archivos_si_no_existen():
    """Crea la carpeta datos y los CSV necesarios para simular la base de datos."""
    try:
        os.makedirs(CARPETA_DATOS, exist_ok=True)

        if not os.path.exists(ARCHIVO_EMPLEADOS) or os.path.getsize(ARCHIVO_EMPLEADOS) == 0:
            with open(ARCHIVO_EMPLEADOS, "w", newline="", encoding="utf-8") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(ENCABEZADO_EMPLEADOS)

        if not os.path.exists(ARCHIVO_SOLICITUDES) or os.path.getsize(ARCHIVO_SOLICITUDES) == 0:
            with open(ARCHIVO_SOLICITUDES, "w", newline="", encoding="utf-8") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(ENCABEZADO_SOLICITUDES)

        cargar_empleados_iniciales_si_esta_vacio()
        actualizar_encabezado_solicitudes_si_es_necesario()
    except OSError as error:
        raise OSError("No se pudieron crear los archivos de datos.") from error


def cargar_empleados_iniciales_si_esta_vacio():
    """Agrega empleados de ejemplo cuando empleados.csv no tiene datos."""
    try:
        with open(ARCHIVO_EMPLEADOS, "r", newline="", encoding="utf-8") as archivo:
            lector = list(csv.reader(archivo))

        if len(lector) <= 1:
            with open(ARCHIVO_EMPLEADOS, "a", newline="", encoding="utf-8") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerows(EMPLEADOS_INICIALES)
    except OSError as error:
        raise OSError("No se pudieron cargar los empleados iniciales.") from error


def actualizar_encabezado_solicitudes_si_es_necesario():
    """Agrega columnas de fecha si solicitudes.csv fue creado con el formato anterior."""
    try:
        with open(ARCHIVO_SOLICITUDES, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            filas = list(lector)
            encabezado_actual = lector.fieldnames

        if encabezado_actual == ENCABEZADO_SOLICITUDES:
            return

        with open(ARCHIVO_SOLICITUDES, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=ENCABEZADO_SOLICITUDES)
            escritor.writeheader()

            for fila in filas:
                escritor.writerow(
                    {
                        "id": fila.get("id", ""),
                        "legajo": fila.get("legajo", ""),
                        "nombre": fila.get("nombre", ""),
                        "dias_solicitados": fila.get("dias_solicitados", ""),
                        "fecha_inicio": fila.get("fecha_inicio", ""),
                        "fecha_fin": fila.get("fecha_fin", ""),
                        "estado": fila.get("estado", ""),
                        "observacion": fila.get("observacion", ""),
                    }
                )
    except OSError as error:
        raise OSError("No se pudo verificar el archivo de solicitudes.") from error


def leer_empleados():
    """Lee los empleados desde el archivo CSV."""
    empleados = []

    try:
        with open(ARCHIVO_EMPLEADOS, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                fila["dias_disponibles"] = int(fila["dias_disponibles"])
                empleados.append(fila)

        return empleados
    except ValueError as error:
        raise ValueError("El archivo de empleados tiene dias disponibles invalidos.") from error
    except OSError as error:
        raise OSError("No se pudo leer el archivo de empleados.") from error


def leer_solicitudes():
    """Lee las solicitudes desde el archivo CSV."""
    try:
        with open(ARCHIVO_SOLICITUDES, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            return list(lector)
    except OSError as error:
        raise OSError("No se pudo leer el archivo de solicitudes.") from error


def buscar_empleado(legajo):
    """Busca un empleado por legajo. Devuelve None si no existe."""
    empleados = leer_empleados()

    for empleado in empleados:
        if empleado["legajo"] == legajo:
            return empleado

    return None


def obtener_proximo_id():
    """Calcula el proximo id para una nueva solicitud."""
    try:
        solicitudes = leer_solicitudes()
        ids = []

        for solicitud in solicitudes:
            if solicitud["id"]:
                ids.append(int(solicitud["id"]))

        if not ids:
            return 1

        return max(ids) + 1
    except ValueError as error:
        raise ValueError("El archivo de solicitudes tiene ids invalidos.") from error


def guardar_solicitud(empleado, dias_solicitados, estado, observacion, fecha_inicio="", fecha_fin=""):
    """Guarda una solicitud de vacaciones en solicitudes.csv."""
    try:
        proximo_id = obtener_proximo_id()

        with open(ARCHIVO_SOLICITUDES, "a", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(
                [
                    proximo_id,
                    empleado["legajo"],
                    empleado["nombre"],
                    dias_solicitados,
                    fecha_inicio,
                    fecha_fin,
                    estado,
                    observacion,
                ]
            )
    except OSError as error:
        raise OSError("No se pudo guardar la solicitud.") from error


def actualizar_estado_solicitud(id_solicitud, estado, observacion):
    """Actualiza el estado de una solicitud existente."""
    solicitudes = leer_solicitudes()
    encontrada = False

    try:
        for solicitud in solicitudes:
            if solicitud["id"] == str(id_solicitud):
                solicitud["estado"] = estado
                solicitud["observacion"] = observacion
                encontrada = True

        if not encontrada:
            raise ValueError("No se encontro la solicitud indicada.")

        with open(ARCHIVO_SOLICITUDES, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=ENCABEZADO_SOLICITUDES)
            escritor.writeheader()
            escritor.writerows(solicitudes)
    except OSError as error:
        raise OSError("No se pudo actualizar la solicitud.") from error


def actualizar_dias_empleado(legajo, dias_solicitados):
    """Descuenta los dias solicitados del saldo del empleado."""
    empleados = leer_empleados()
    empleado_encontrado = False

    try:
        for empleado in empleados:
            if empleado["legajo"] == legajo:
                empleado_encontrado = True

                if dias_solicitados > empleado["dias_disponibles"]:
                    raise ValueError("No se pueden descontar mas dias de los disponibles.")

                empleado["dias_disponibles"] -= dias_solicitados

        if not empleado_encontrado:
            raise ValueError("No existe un empleado con ese legajo.")

        with open(ARCHIVO_EMPLEADOS, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=ENCABEZADO_EMPLEADOS)
            escritor.writeheader()
            escritor.writerows(empleados)
    except OSError as error:
        raise OSError("No se pudo actualizar el saldo del empleado.") from error


def pedir_numero(mensaje):
    """Pide un numero entero mayor a cero."""
    while True:
        dato = input(mensaje)

        try:
            numero = int(dato)

            if numero <= 0:
                raise ValueError("La cantidad debe ser mayor a 0.")

            return numero
        except ValueError:
            print("Dato invalido. Ingrese un numero entero mayor a 0.")


def pedir_fecha(mensaje):
    """Pide una fecha con formato DD/MM/AAAA."""
    while True:
        dato = input(mensaje).strip()

        try:
            fecha = datetime.strptime(dato, FORMATO_FECHA).date()

            if fecha < datetime.today().date():
                raise ValueError("La fecha no puede ser anterior al dia actual.")

            return fecha
        except ValueError:
            print("Fecha invalida. Ingrese una fecha valida con formato DD/MM/AAAA.")


def pedir_respuesta_supervisor():
    """Pide la decision del supervisor y acepta solamente S o N."""
    while True:
        respuesta = input("Supervisor, aprueba la solicitud? (S/N): ").strip().upper()

        if respuesta in ["S", "N"]:
            return respuesta

        print("Respuesta invalida. Ingrese S para aprobar o N para rechazar.")


def calcular_fecha_fin(fecha_inicio, dias_solicitados):
    """Calcula la fecha final tomando dias corridos."""
    fecha_fin = fecha_inicio + timedelta(days=dias_solicitados - 1)
    return fecha_fin


def fechas_se_superponen(inicio_1, fin_1, inicio_2, fin_2):
    """Valida si dos rangos de fechas se pisan."""
    return inicio_1 <= fin_2 and inicio_2 <= fin_1


def fechas_disponibles(fecha_inicio, fecha_fin, id_solicitud_a_ignorar=""):
    """Controla que no haya otro empleado con vacaciones en la misma fecha."""
    solicitudes = leer_solicitudes()

    for solicitud in solicitudes:
        if solicitud["id"] == str(id_solicitud_a_ignorar):
            continue

        if solicitud["estado"] not in [ESTADO_APROBADA, ESTADO_PENDIENTE]:
            continue

        if not solicitud["fecha_inicio"] or not solicitud["fecha_fin"]:
            continue

        inicio_existente = datetime.strptime(solicitud["fecha_inicio"], FORMATO_FECHA).date()
        fin_existente = datetime.strptime(solicitud["fecha_fin"], FORMATO_FECHA).date()

        if fechas_se_superponen(fecha_inicio, fecha_fin, inicio_existente, fin_existente):
            return False

    return True


def mostrar_solicitudes_pendientes_empleado(legajo):
    """Muestra las solicitudes pendientes de un empleado."""
    solicitudes = leer_solicitudes()
    pendientes = []

    for solicitud in solicitudes:
        if solicitud["legajo"] == legajo and solicitud["estado"] == ESTADO_PENDIENTE:
            pendientes.append(solicitud)

    if not pendientes:
        print("Chatbot: no tiene solicitudes pendientes.")
        return

    print("Chatbot: solicitudes pendientes:")
    for solicitud in pendientes:
        print(
            f"- ID {solicitud['id']}: {solicitud['dias_solicitados']} dias "
            f"del {solicitud['fecha_inicio']} al {solicitud['fecha_fin']}"
        )


def obtener_solicitudes_pendientes_supervisor():
    """Obtiene las solicitudes que debe revisar el supervisor."""
    solicitudes = leer_solicitudes()
    pendientes = []

    for solicitud in solicitudes:
        if solicitud["estado"] == ESTADO_PENDIENTE:
            pendientes.append(solicitud)

    return pendientes


def iniciar_chatbot():
    """Ejecuta el sistema con seleccion de rol."""
    print("=== Sistema de Gestion de Vacaciones ===")

    while True:
        print("\nMenu principal")
        print("1 - Ingresar como empleado")
        print("2 - Ingresar como supervisor")
        print("0 - Salir")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "0":
            print("Sistema: gracias por utilizar el sistema. Hasta luego.")
            break

        try:
            crear_archivos_si_no_existen()

            if opcion == "1":
                menu_empleado()
            elif opcion == "2":
                menu_supervisor()
            else:
                print("Opcion invalida. Ingrese 1, 2 o 0.")
        except (OSError, ValueError) as error:
            print(f"Error: {error}")
            print("Sistema: no se pudo completar la operacion. Volviendo al menu principal.")


def menu_empleado():
    """Permite al empleado consultar pendientes y crear una solicitud."""
    print("\nEmpleado: ingreso al sistema.")

    legajo = input("Chatbot: ingrese su legajo: ").strip()
    empleado = buscar_empleado(legajo)

    if empleado is None:
        empleado_inexistente = {
            "legajo": legajo,
            "nombre": "Empleado inexistente",
            "dias_disponibles": 0,
        }
        guardar_solicitud(
            empleado_inexistente,
            0,
            ESTADO_EMPLEADO_INEXISTENTE,
            "El legajo ingresado no existe en el sistema.",
        )
        print("Chatbot: el empleado no existe en el sistema.")
        return

    print(f"Chatbot: bienvenido/a, {empleado['nombre']}.")
    print(f"Chatbot: dias disponibles: {empleado['dias_disponibles']}.")
    mostrar_solicitudes_pendientes_empleado(legajo)

    while True:
        print("\nMenu empleado")
        print("1 - Nueva solicitud de vacaciones")
        print("0 - Volver al menu principal")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "0":
            return

        if opcion == "1":
            ejecutar_solicitud_vacaciones(empleado)
            return

        print("Opcion invalida. Ingrese 1 para solicitar vacaciones o 0 para volver.")


def ejecutar_solicitud_vacaciones(empleado):
    """Ejecuta una solicitud individual de vacaciones."""
    print("\nEmpleado: inicio del proceso de solicitud.")

    fecha_inicio = pedir_fecha("Chatbot: ingrese fecha de inicio (DD/MM/AAAA): ")
    dias_solicitados = pedir_numero("Chatbot: cuantos dias desea solicitar?: ")
    fecha_fin = calcular_fecha_fin(fecha_inicio, dias_solicitados)

    fecha_inicio_texto = fecha_inicio.strftime(FORMATO_FECHA)
    fecha_fin_texto = fecha_fin.strftime(FORMATO_FECHA)

    if dias_solicitados > empleado["dias_disponibles"]:
        guardar_solicitud(
            empleado,
            dias_solicitados,
            ESTADO_RECHAZADA_SALDO,
            "El empleado no tiene saldo suficiente.",
            fecha_inicio_texto,
            fecha_fin_texto,
        )
        print("Chatbot: saldo insuficiente. Solicitud rechazada.")
        return

    if not fechas_disponibles(fecha_inicio, fecha_fin):
        guardar_solicitud(
            empleado,
            dias_solicitados,
            ESTADO_RECHAZADA_SUPERVISOR,
            "La fecha solicitada no esta disponible.",
            fecha_inicio_texto,
            fecha_fin_texto,
        )
        print("Chatbot: la fecha solicitada no esta disponible.")
        return

    guardar_solicitud(
        empleado,
        dias_solicitados,
        ESTADO_PENDIENTE,
        "Solicitud enviada al supervisor.",
        fecha_inicio_texto,
        fecha_fin_texto,
    )

    print("Chatbot: solicitud registrada y enviada al supervisor.")
    print(f"Chatbot: periodo solicitado: {fecha_inicio_texto} al {fecha_fin_texto}.")


def menu_supervisor():
    """Permite al supervisor aprobar o rechazar solicitudes pendientes."""
    print("\nSupervisor: ingreso al sistema.")
    pendientes = obtener_solicitudes_pendientes_supervisor()

    if not pendientes:
        print("Supervisor: no hay solicitudes pendientes para revisar.")
        return

    print("Supervisor: solicitudes pendientes de aprobacion:")

    for solicitud in pendientes:
        print(
            f"\nID {solicitud['id']} - {solicitud['nombre']} "
            f"({solicitud['legajo']})"
        )
        print(
            f"Dias: {solicitud['dias_solicitados']} - "
            f"Desde {solicitud['fecha_inicio']} hasta {solicitud['fecha_fin']}"
        )

        respuesta = pedir_respuesta_supervisor()

        if respuesta == "N":
            actualizar_estado_solicitud(
                solicitud["id"],
                ESTADO_RECHAZADA_SUPERVISOR,
                "El supervisor rechazo la solicitud.",
            )
            print("Supervisor: solicitud rechazada.")
            continue

        aprobar_solicitud_supervisor(solicitud)


def aprobar_solicitud_supervisor(solicitud):
    """Aprueba una solicitud pendiente y descuenta los dias del empleado."""
    empleado = buscar_empleado(solicitud["legajo"])

    if empleado is None:
        actualizar_estado_solicitud(
            solicitud["id"],
            ESTADO_EMPLEADO_INEXISTENTE,
            "El empleado ya no existe en el sistema.",
        )
        print("Supervisor: el empleado no existe. Solicitud actualizada.")
        return

    dias_solicitados = int(solicitud["dias_solicitados"])
    fecha_inicio = datetime.strptime(solicitud["fecha_inicio"], FORMATO_FECHA).date()
    fecha_fin = datetime.strptime(solicitud["fecha_fin"], FORMATO_FECHA).date()

    if dias_solicitados > empleado["dias_disponibles"]:
        actualizar_estado_solicitud(
            solicitud["id"],
            ESTADO_RECHAZADA_SALDO,
            "El empleado ya no tiene saldo suficiente.",
        )
        print("Supervisor: saldo insuficiente. Solicitud rechazada.")
        return

    if not fechas_disponibles(fecha_inicio, fecha_fin, solicitud["id"]):
        actualizar_estado_solicitud(
            solicitud["id"],
            ESTADO_RECHAZADA_SUPERVISOR,
            "La fecha solicitada ya no esta disponible.",
        )
        print("Supervisor: la fecha ya no esta disponible. Solicitud rechazada.")
        return

    actualizar_dias_empleado(solicitud["legajo"], dias_solicitados)
    actualizar_estado_solicitud(
        solicitud["id"],
        ESTADO_APROBADA,
        "El supervisor aprobo la solicitud.",
    )
    print("Supervisor: solicitud aprobada y dias descontados.")


if __name__ == "__main__":
    iniciar_chatbot()
