import csv
import os

RUTA_EMPLEADOS = "datos/empleados.csv"
RUTA_SOLICITUDES = "datos/solicitudes.csv"


def leer_empleados():
    try:
        if not os.path.exists(RUTA_EMPLEADOS):
            raise FileNotFoundError("No existe el archivo de empleados.")

        empleados = []

        with open(RUTA_EMPLEADOS, "r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                empleado = {
                    "legajo": fila["legajo"],
                    "nombre": fila["nombre"],
                    "dias_disponibles": int(fila["dias_disponibles"])
                }

                empleados.append(empleado)

        if len(empleados) == 0:
            raise ValueError("No hay empleados cargados.")

        return empleados

    except FileNotFoundError as error:
        print(f"Error: {error}")
        return []

    except ValueError as error:
        print(f"Error: {error}")
        return []

    except Exception as error:
        print(f"Error inesperado al leer empleados: {error}")
        return []


def buscar_empleado(legajo, empleados):
    try:
        if legajo == "":
            raise ValueError("El legajo no puede estar vacio.")

        for empleado in empleados:
            if empleado["legajo"] == legajo:
                return empleado

        raise ValueError("El empleado no existe en el sistema.")

    except ValueError as error:
        print(f"Error: {error}")
        return None


def obtener_proximo_id():
    try:
        if not os.path.exists(RUTA_SOLICITUDES):
            return 1

        with open(RUTA_SOLICITUDES, "r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            solicitudes = list(lector)

            if len(solicitudes) == 0:
                return 1

            ultimo_id = int(solicitudes[-1]["id"])
            return ultimo_id + 1

    except Exception as error:
        print(f"Error al obtener el proximo ID: {error}")
        return 1


def guardar_solicitud(empleado, dias_solicitados, estado):
    try:
        if empleado is None:
            raise ValueError("No se puede guardar una solicitud sin empleado.")

        if dias_solicitados <= 0:
            raise ValueError("Los dias solicitados deben ser mayores a 0.")

        if estado == "":
            raise ValueError("El estado de la solicitud no puede estar vacio.")

        existe_archivo = os.path.exists(RUTA_SOLICITUDES)
        proximo_id = obtener_proximo_id()

        with open(RUTA_SOLICITUDES, "a", newline="", encoding="utf-8") as archivo:
            campos = ["id", "legajo", "nombre", "dias_solicitados", "estado"]
            escritor = csv.DictWriter(archivo, fieldnames=campos)

            if not existe_archivo:
                escritor.writeheader()

            escritor.writerow({
                "id": proximo_id,
                "legajo": empleado["legajo"],
                "nombre": empleado["nombre"],
                "dias_solicitados": dias_solicitados,
                "estado": estado
            })

    except ValueError as error:
        print(f"Error: {error}")

    except Exception as error:
        print(f"Error inesperado al guardar la solicitud: {error}")


def actualizar_dias_empleado(legajo, dias_solicitados):
    try:
        if legajo == "":
            raise ValueError("El legajo no puede estar vacio.")

        if dias_solicitados <= 0:
            raise ValueError("Los dias solicitados deben ser mayores a 0.")

        empleados = leer_empleados()
        empleado_encontrado = False

        for empleado in empleados:
            if empleado["legajo"] == legajo:
                empleado_encontrado = True

                if dias_solicitados > empleado["dias_disponibles"]:
                    raise ValueError("No se pueden descontar mas dias de los disponibles.")

                empleado["dias_disponibles"] -= dias_solicitados

        if not empleado_encontrado:
            raise ValueError("No se encontro el empleado para actualizar dias.")

        with open(RUTA_EMPLEADOS, "w", newline="", encoding="utf-8") as archivo:
            campos = ["legajo", "nombre", "dias_disponibles"]
            escritor = csv.DictWriter(archivo, fieldnames=campos)

            escritor.writeheader()

            for empleado in empleados:
                escritor.writerow(empleado)

    except ValueError as error:
        print(f"Error: {error}")

    except Exception as error:
        print(f"Error inesperado al actualizar dias: {error}")


def pedir_numero(mensaje):
    while True:
        try:
            entrada = input(mensaje).strip()

            if entrada == "":
                raise ValueError("El campo no puede estar vacio.")

            numero = int(entrada)

            if numero <= 0:
                raise ValueError("El numero debe ser mayor a 0.")

            return numero

        except ValueError as error:
            print(f"Error: {error}")


def pedir_respuesta_supervisor():
    while True:
        try:
            respuesta = input("El supervisor aprueba la solicitud? (S/N): ").strip().upper()

            if respuesta == "":
                raise ValueError("La respuesta no puede estar vacia.")

            if respuesta != "S" and respuesta != "N":
                raise ValueError("Debe ingresar S para aprobar o N para rechazar.")

            return respuesta

        except ValueError as error:
            print(f"Error: {error}")


def iniciar_chatbot():
    try:
        print("Bienvenido al chatbot de gestion de vacaciones")
        print("---------------------------------------------")

        empleados = leer_empleados()

        if len(empleados) == 0:
            raise ValueError("No se puede iniciar el chatbot sin empleados cargados.")

        legajo = input("Ingrese su legajo: ").strip()

        empleado = buscar_empleado(legajo, empleados)

        if empleado is None:
            raise ValueError("No se puede continuar con la solicitud.")

        print(f"Hola {empleado['nombre']}")
        print(f"Dias disponibles: {empleado['dias_disponibles']}")

        dias_solicitados = pedir_numero("Ingrese la cantidad de dias que desea solicitar: ")

        if dias_solicitados > empleado["dias_disponibles"]:
            print("Saldo insuficiente para realizar la solicitud.")
            guardar_solicitud(empleado, dias_solicitados, "RECHAZADA - SALDO INSUFICIENTE")
            return

        print("Solicitud registrada correctamente.")
        print("Enviando solicitud al supervisor...")

        respuesta = pedir_respuesta_supervisor()

        if respuesta == "S":
            actualizar_dias_empleado(empleado["legajo"], dias_solicitados)
            guardar_solicitud(empleado, dias_solicitados, "APROBADA")

            print("Solicitud aprobada.")
            print("Se descontaron los dias del saldo disponible.")

        else:
            guardar_solicitud(empleado, dias_solicitados, "RECHAZADA POR SUPERVISOR")
            print("Solicitud rechazada por el supervisor.")

        print("Fin del proceso.")

    except ValueError as error:
        print(f"Error: {error}")

    except Exception as error:
        print(f"Error inesperado en el chatbot: {error}")


iniciar_chatbot()