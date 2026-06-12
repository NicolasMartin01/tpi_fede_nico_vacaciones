import csv
import os

from constantes import ( ARCHIVO_EMPLEADOS,ARCHIVO_SOLICITUDES,CARPETA_DATOS,EMPLEADOS_INICIALES,ENCABEZADO_EMPLEADOS,ENCABEZADO_SOLICITUDES,)


def crear_archivos():
  """Crea los archivos CSV si no existen."""
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

    cargar_empleados()
    acomodar_solicitudes()
  except OSError as error:
    raise OSError("No se pudieron crear los archivos.") from error


def cargar_empleados():
  """Carga empleados de ejemplo si el archivo esta vacio."""
  try:
    with open(ARCHIVO_EMPLEADOS, "r", newline="", encoding="utf-8") as archivo:
      filas = list(csv.reader(archivo))

    if len(filas) <= 1:
      with open(ARCHIVO_EMPLEADOS, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(EMPLEADOS_INICIALES)
  except OSError as error:
    raise OSError("No se pudieron cargar los empleados.") from error


def acomodar_solicitudes():
  """Deja solicitudes.csv con el formato simple del BPMN."""
  try:
    with open(ARCHIVO_SOLICITUDES, "r", newline="", encoding="utf-8") as archivo:
      lector = csv.DictReader(archivo)
      filas = list(lector)
      encabezado = lector.fieldnames

    if encabezado == ENCABEZADO_SOLICITUDES:
      return

    with open(ARCHIVO_SOLICITUDES, "w", newline="", encoding="utf-8") as archivo:
      escritor = csv.DictWriter(archivo, fieldnames=ENCABEZADO_SOLICITUDES)
      escritor.writeheader()

      for fila in filas:
        escritor.writerow({
          "id": fila.get("id", ""),
          "legajo": fila.get("legajo", ""),
          "nombre": fila.get("nombre", ""),
          "dias": fila.get("dias", fila.get("dias_solicitados", "")),
          "estado": fila.get("estado", ""),
          "observacion": fila.get("observacion", ""),
        })
  except OSError as error:
    raise OSError("No se pudo revisar el archivo de solicitudes.") from error


def leer_empleados():
  """Lee empleados.csv."""
  empleados = []

  try:
    with open(ARCHIVO_EMPLEADOS, "r", newline="", encoding="utf-8") as archivo:
      lector = csv.DictReader(archivo)

      for fila in lector:
        fila["dias_disponibles"] = int(fila["dias_disponibles"])
        empleados.append(fila)

    return empleados
  except ValueError as error:
    raise ValueError("Hay dias disponibles invalidos.") from error
  except OSError as error:
    raise OSError("No se pudo leer empleados.csv.") from error


def leer_solicitudes():
  """Lee solicitudes.csv."""
  try:
    with open(ARCHIVO_SOLICITUDES, "r", newline="", encoding="utf-8") as archivo:
      lector = csv.DictReader(archivo)
      return list(lector)
  except OSError as error:
    raise OSError("No se pudo leer solicitudes.csv.") from error


def buscar_empleado(legajo):
  """Busca un empleado por legajo."""
  empleados = leer_empleados()

  for empleado in empleados:
    if empleado["legajo"] == legajo:
      return empleado

  return None


def verificar_contrasena(empleado, contrasena):
  """Verifica que la contraseña coincida con la del empleado."""
  return empleado["contrasena"] == contrasena


def proximo_id():
  """Devuelve el proximo id de solicitud."""
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
    raise ValueError("Hay ids invalidos en solicitudes.csv.") from error


def guardar_solicitud(empleado, dias, estado, observacion):
  """Guarda una solicitud."""
  try:
    id_solicitud = proximo_id()

    with open(ARCHIVO_SOLICITUDES, "a", newline="", encoding="utf-8") as archivo:
      escritor = csv.writer(archivo)
      escritor.writerow([
        id_solicitud,
        empleado["legajo"],
        empleado["nombre"],
        dias,
        estado,
        observacion,
      ])

    return id_solicitud
  except OSError as error:
    raise OSError("No se pudo guardar la solicitud.") from error


def cambiar_estado(id_solicitud, estado, observacion):
  """Cambia el estado de una solicitud."""
  solicitudes = leer_solicitudes()
  encontrada = False

  try:
    for solicitud in solicitudes:
      if solicitud["id"] == str(id_solicitud):
        solicitud["estado"] = estado
        solicitud["observacion"] = observacion
        encontrada = True

    if not encontrada:
      raise ValueError("No se encontro la solicitud.")

    with open(ARCHIVO_SOLICITUDES, "w", newline="", encoding="utf-8") as archivo:
      escritor = csv.DictWriter(archivo, fieldnames=ENCABEZADO_SOLICITUDES)
      escritor.writeheader()
      escritor.writerows(solicitudes)
  except OSError as error:
    raise OSError("No se pudo actualizar la solicitud.") from error


def descontar_dias(legajo, dias):
  """Descuenta dias al empleado."""
  empleados = leer_empleados()
  encontrado = False

  try:
    for empleado in empleados:
      if empleado["legajo"] == legajo:
        empleado["dias_disponibles"] -= dias
        encontrado = True

    if not encontrado:
      raise ValueError("No se encontro el empleado.")

    with open(ARCHIVO_EMPLEADOS, "w", newline="", encoding="utf-8") as archivo:
      escritor = csv.DictWriter(archivo, fieldnames=ENCABEZADO_EMPLEADOS)
      escritor.writeheader()
      escritor.writerows(empleados)
  except OSError as error:
    raise OSError("No se pudo actualizar empleados.csv.") from error
