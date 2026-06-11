def pedir_legajo():
  """Pide el legajo."""
  while True:
    legajo = input("Chatbot: ingrese su legajo: ").strip()

    if legajo:
      return legajo

    print("Chatbot: el legajo no puede estar vacio.")


def pedir_numero(mensaje):
  """Pide un numero mayor a cero."""
  while True:
    dato = input(mensaje).strip()

    try:
      numero = int(dato)

      if numero <= 0:
        raise ValueError

      return numero
    except ValueError:
      print("Chatbot: ingrese un numero entero mayor a 0.")


def pedir_respuesta():
  """Pide la respuesta del supervisor."""
  while True:
    respuesta = input("Supervisor, aprueba la solicitud? (S/N): ").strip().upper()

    if respuesta in ["S", "N"]:
      return respuesta

    print("Supervisor: ingrese S para aprobar o N para rechazar.")
