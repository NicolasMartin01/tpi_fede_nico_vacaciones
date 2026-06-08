from archivos import buscar_empleado
from archivos import cambiar_estado
from archivos import crear_archivos
from archivos import descontar_dias
from archivos import guardar_solicitud
from constantes import ESTADO_APROBADA
from constantes import ESTADO_EMPLEADO_INEXISTENTE
from constantes import ESTADO_PENDIENTE
from constantes import ESTADO_RECHAZADA_SALDO
from constantes import ESTADO_RECHAZADA_SUPERVISOR
from validaciones import pedir_legajo, pedir_numero, pedir_respuesta


def iniciar_chatbot():
  """Ejecuta el flujo del BPMN."""
  print("=== Chatbot de Gestion de Vacaciones ===")

  try:
    crear_archivos()
    legajo = pedir_legajo()
    empleado = buscar_empleado(legajo)

    if empleado is None:
      empleado_error = {
        "legajo": legajo,
        "nombre": "Empleado inexistente",
      }
      guardar_solicitud(
        empleado_error,
        0,
        ESTADO_EMPLEADO_INEXISTENTE,
        "El legajo no existe.",
      )
      print("Chatbot: el empleado no existe. Se registro el intento.")
      return

    print(f"Chatbot: empleado encontrado: {empleado['nombre']}.")
    print(f"Chatbot: dias disponibles: {empleado['dias_disponibles']}.")

    dias = pedir_numero("Chatbot: cuantos dias desea solicitar?: ")

    if dias > empleado["dias_disponibles"]:
      guardar_solicitud(
        empleado,
        dias,
        ESTADO_RECHAZADA_SALDO,
        "Saldo insuficiente.",
      )
      print("Chatbot: saldo insuficiente. Solicitud rechazada.")
      return

    id_solicitud = guardar_solicitud(
      empleado,
      dias,
      ESTADO_PENDIENTE,
      "Solicitud enviada al supervisor.",
    )

    print("Chatbot: solicitud registrada y enviada al supervisor.")

    respuesta = pedir_respuesta()

    if respuesta == "S":
      aprobar_solicitud(id_solicitud, empleado, dias)
    else:
      rechazar_solicitud(id_solicitud)
  except (OSError, ValueError) as error:
    print(f"Error: {error}")


def aprobar_solicitud(id_solicitud, empleado, dias):
  """Aprueba la solicitud."""
  descontar_dias(empleado["legajo"], dias)
  cambiar_estado(
    id_solicitud,
    ESTADO_APROBADA,
    "El supervisor aprobo la solicitud.",
  )
  print("Supervisor: solicitud aprobada.")
  print("Chatbot: dias descontados correctamente.")


def rechazar_solicitud(id_solicitud):
  """Rechaza la solicitud."""
  cambiar_estado(
    id_solicitud,
    ESTADO_RECHAZADA_SUPERVISOR,
    "El supervisor rechazo la solicitud.",
  )
  print("Supervisor: solicitud rechazada.")
  print("Chatbot: se registro el rechazo.")


if __name__ == "__main__":
  iniciar_chatbot()
