import re
import time
import random


def leer_expresiones_regulares(ruta_archivo="chatbot/expresiones_chatbot_hoteles.csv"):
    patrones = {}
    pesos = {}
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        for i, linea in enumerate(archivo):
            if i == 0:
                continue  # Saltar encabezado
            linea = linea.strip()
            if linea:
                partes = linea.split(",", 2)
                if len(partes) == 3:
                    intencion, patron, peso = partes
                    patrones[intencion.strip()] = re.compile(
                        patron.strip(), re.IGNORECASE
                    )
                    try:
                        pesos[intencion.strip()] = int(peso.strip())
                    except:
                        pesos[intencion.strip()] = 1
    return patrones, pesos


def chatbot_hoteles(patrones, pesos):
    state = 0
    contexto = {
        "nombre": None,
        "correo": None,
        "telefono": None,
        "fecha": None,
        "habitacion": None,
        "servicios": [],
        "personas": None,
        "preferencias": None,
        "num_reserva": None,
    }
    print("Hola soy Hoss el Chatbot de Hoteles. ¿En qué te puedo ayudar?")
    print("Puedes preguntarme sobre:")
    print("- Reservar una habitación")
    print("- Cancelar una reservación")
    print("- Modificar tu reservación (fecha, nombre, habitación)")
    print("- Precios y tarifas")
    print("- Servicios del hotel")
    print("- Disponibilidad de habitaciones")
    print("- Ubicación y cómo llegar")
    print("- Horarios de check-in y check-out")
    print("- Transferencias de pago")
    time.sleep(1)
    while True:
        if state == 0:
            entrada = input("Tú: ").strip().lower()
            if entrada in ["salir", "exit", "quit"]:
                print("Hoss: ¡Hasta luego!")
                break
            pesos_detectados = {}
            for key, patron in patrones.items():
                coincidencias = 1 if patron.search(entrada) else 0
                pesos_detectados[key] = coincidencias * pesos.get(key, 1)
            intencion_detectada = (
                max(pesos_detectados, key=pesos_detectados.get)
                if any(pesos_detectados.values())
                else None
            )
            # Desambiguación y manejo de errores
            if not intencion_detectada:
                print(
                    "Hoss: No entendí tu solicitud. Ejemplos: 'Quiero reservar', '¿Cuánto cuesta?', '¿Tienen wifi?', '¿Aceptan mascotas?'. ¿Puedes reformular?"
                )
                continue
            if intencion_detectada == "saludo":
                print("Hoss: ¡Hola! ¿En qué puedo ayudarte hoy?")
            elif intencion_detectada == "despedida":
                print("Hoss: Gracias por contactarnos. ¡Hasta luego!")
                return
            elif intencion_detectada == "reservar":
                state = 1
            elif intencion_detectada == "cancelar":
                print("Hoss: ¿Puedes darme el número de reserva que deseas cancelar?")
                state = 2
            elif intencion_detectada == "modificar":
                print(
                    "Hoss: ¿Qué cambio deseas realizar en tu reserva? (fecha, nombre, habitación)"
                )
                state = 3
            elif intencion_detectada in ["precio", "precio_habitacion"]:
                state = 4
            elif intencion_detectada == "afirmacion" and state == 4:
                print(
                    "Hoss: Opciones de precios: Habitación sencilla $800, doble $1200, suite $2000 por noche. ¿Te gustaría reservar alguna?"
                )
                state = 0
            elif intencion_detectada == "servicios":
                print(
                    "Hoss: Ofrecemos wifi, desayuno, spa, piscina y más. ¿Te interesa algún servicio en particular?"
                )
                servicio = input("¿Qué servicio te interesa?: ").strip().lower()
                contexto["servicios"].append(servicio)
                print(
                    f"Hoss: Servicio '{servicio}' registrado. ¿Te puedo ayudar en algo más?"
                )
            elif intencion_detectada == "disponibilidad":
                personas = input("¿Para cuántas personas buscas habitación?: ").strip()
                contexto["personas"] = personas
                fecha = input("¿Para qué fechas?: ").strip()
                contexto["fecha"] = fecha
                print(
                    f"Hoss: Buscando disponibilidad para {personas} personas en la fecha {fecha}..."
                )
            elif intencion_detectada == "ubicacion":
                print(
                    "Hoss: Estamos en el centro de la ciudad, cerca de los principales atractivos. ¿Necesitas indicaciones?"
                )
            elif intencion_detectada == "checkin_checkout":
                print(
                    "Hoss: El check-in es a partir de las 14:00 y el check-out hasta las 12:00. ¿Te gustaría reservar?"
                )
            elif intencion_detectada == "agradecimiento":
                print("Hoss: ¡Estamos para servirte!")
            # Personalización y datos clave
            elif intencion_detectada in [
                "nombre",
                "correo",
                "telefono",
                "preferencias",
            ]:
                dato = input(
                    f"Por favor, proporciona tu {intencion_detectada}: "
                ).strip()
                contexto[intencion_detectada] = dato
                print(
                    f"Hoss: {intencion_detectada.capitalize()} registrado. ¿Te puedo ayudar en algo más?"
                )
            else:
                print(
                    "Hoss: No entendí tu solicitud. Ejemplos: 'Quiero reservar', '¿Cuánto cuesta?', '¿Tienen wifi?', '¿Aceptan mascotas?'. ¿Puedes reformular?"
                )
        elif state == 1:
            fecha = input(
                "Hoss: ¿Para qué fecha deseas la reserva? (dd/mm/aaaa): "
            ).strip()
            contexto["fecha"] = fecha
            nombre = input("Hoss: ¿A nombre de quién será la reserva?: ").strip()
            contexto["nombre"] = nombre
            personas = input("Hoss: ¿Para cuántas personas?: ").strip()
            contexto["personas"] = personas
            habitacion = (
                input(
                    "Hoss: ¿Qué tipo de habitación prefieres (sencilla, doble, suite)?: "
                )
                .strip()
                .lower()
            )
            contexto["habitacion"] = habitacion
            print(
                f"Hoss: Reserva para {nombre}, fecha {fecha}, {personas} personas, habitación {habitacion}. ¿Deseas confirmar la reserva? (sí/no)"
            )
            confirm = input("Confirmar reserva: ").strip().lower()
            patron_afirmacion = patrones.get("afirmacion")
            if patron_afirmacion and patron_afirmacion.search(confirm):
                num_reserva = random.randint(100000, 999999)
                contexto["num_reserva"] = num_reserva
                print(
                    f"Hoss: ¡Reserva confirmada! Tu número de reserva es {num_reserva}. ¿Te puedo ayudar en algo más?"
                )
            else:
                print("Hoss: Reserva no confirmada. ¿Te puedo ayudar en algo más?")
            state = 0
        elif state == 3:
            cambio = (
                input("¿Qué cambio deseas realizar? (fecha, nombre, habitación): ")
                .strip()
                .lower()
            )
            respuesta_mod = ""
            tipo_mod = None
            for mod_key in [
                "modificar_fecha",
                "modificar_nombre",
                "modificar_habitacion",
            ]:
                patron_mod = patrones.get(mod_key)
                if patron_mod and patron_mod.search(cambio):
                    tipo_mod = mod_key
                    break
            if tipo_mod == "modificar_fecha":
                nueva_fecha = input("¿Cuál es la nueva fecha?: ").strip()
                contexto["fecha"] = nueva_fecha
                respuesta_mod += f"La fecha será actualizada a {nueva_fecha}. "
            elif tipo_mod == "modificar_nombre":
                nuevo_nombre = input("¿Cuál es el nuevo nombre?: ").strip()
                contexto["nombre"] = nuevo_nombre
                respuesta_mod += f"El nombre será actualizado a {nuevo_nombre}. "
            elif tipo_mod == "modificar_habitacion":
                nueva_hab = (
                    input("¿Qué tipo de habitación prefieres?: ").strip().lower()
                )
                contexto["habitacion"] = nueva_hab
                respuesta_mod += f"La habitación será modificada a {nueva_hab}. "
            else:
                respuesta_mod += cambio.capitalize() + ". "
            print(f"Hoss: {respuesta_mod} ¿Deseas confirmar el cambio? (sí/no)")
            confirm = input("Confirmar cambio: ").strip().lower()
            patron_afirmacion = patrones.get("afirmacion")
            if patron_afirmacion and patron_afirmacion.search(confirm):
                print("Hoss: ¡Cambio confirmado! ¿Te puedo ayudar en algo más?")
            else:
                print("Hoss: Cambio no realizado. ¿Te puedo ayudar en algo más?")
            state = 0
        elif state == 2:
            num_reserva = input("Número de reserva a cancelar: ")
            print(
                f"Hoss: Cancelación registrada para la reserva {num_reserva}. ¿Te puedo ayudar en algo más?"
            )
            state = 0
        elif state == 4:
            while True:
                respuesta_hab = (
                    input(
                        "Hoss: El precio depende de la temporada y tipo de habitación.\n¿Qué tipo de habitación te interesa (sencilla, doble, suite)?: "
                    )
                    .strip()
                    .lower()
                )
                tipo_hab = None
                if patrones["tipo_habitacion_sencilla"].search(respuesta_hab):
                    tipo_hab = "sencilla"
                elif patrones["tipo_habitacion_doble"].search(respuesta_hab):
                    tipo_hab = "doble"
                elif patrones["tipo_habitacion_suite"].search(respuesta_hab):
                    tipo_hab = "suite"
                contexto["habitacion"] = tipo_hab if tipo_hab else respuesta_hab
                print(
                    f"Hoss: Precios para habitación {tipo_hab if tipo_hab else respuesta_hab}: "
                )
                if tipo_hab == "sencilla":
                    print("Hoss: Habitación sencilla $800 por noche.")
                elif tipo_hab == "doble":
                    print("Hoss: Habitación doble $1200 por noche.")
                elif tipo_hab == "suite":
                    print("Hoss: Suite $2000 por noche.")
                else:
                    print(
                        "Hoss: No tengo información para ese tipo de habitación, pero puedo mostrarte opciones generales: sencilla $800, doble $1200, suite $2000 por noche."
                    )
                print("¿Te gustaría reservar esta habitación? (sí/no)")
                respuesta = input("Confirmar reserva: ").strip().lower()
                patron_afirmacion = patrones.get("afirmacion")
                if patron_afirmacion and patron_afirmacion.search(respuesta):
                    print(
                        f"Hoss: Perfecto, vamos a realizar la reservación de la habitación. Te haré unas preguntas para completar la reserva."
                    )
                    state = 1
                    break
                elif respuesta in ["no", "n", "no gracias", "ninguna"]:
                    print("Hoss: Reserva no realizada. ¿Te puedo ayudar en algo más?")
                    state = 0
                    break
                else:
                    print(
                        "Hoss: Puedes preguntar por otra habitación o escribir 'no' para salir."
                    )


if __name__ == "__main__":
    patrones, pesos = leer_expresiones_regulares()
    chatbot_hoteles(patrones, pesos)
