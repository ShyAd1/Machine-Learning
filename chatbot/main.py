import re
import time
import random
import csv


desayunos_op = [
    "huevos al gusto",
    "panqueques con jarabe de arce",
    "yogur con granola y frutas",
    "tostadas de aguacate",
    "batido de proteínas",
    "gachas de avena con bayas",
    "burrito",
    "croissant",
    "chilaquiles",
    "hot cakes",
    "pozole",
    "barbacoa(fines de semana)",
]

bebidas_op = [
    "jugo de naranja",
    "café",
    "té",
    "leche",
    "batido de frutas",
    "agua",
    "vodka tonik",
    "carajillo",
    "refrescos",
]

bebidas_alc = [
    "azulito",
    "lean",
    "thom collins (solo para paladares educados)",
    "cerveza[s] (variedad)",
    "tequila",
    "cantarito",
    "vino tinto",
    "vino blanco",
    "ron",
    "vodka",
    "whisky",
    "gin",
    "margarita",
    "mojito",
    "cosmopolitan",
    "old fashioned",
    "daiquiri",
    "beileys de pobres",
    "bucaña",
    "amazul",
]

comidas_op = [
    "pizza",
    "pasta",
    "hamburguesas",
    "tacos",
    "sushi",
    "ensalada",
    "sopa",
    "pollo asado",
    "filete de carne",
    "mariscos",
]

act_niños = [
    "juegos en la piscina",
    "manualidades y dibujo",
    "mini club infantil",
    "clases de cocina para niños",
    "búsqueda del tesoro",
    "noche de cine con palomitas",
    "deportes en el jardín (fútbol, voleibol)",
    "espectáculos de magia o marionetas",
    "sesión de karaoke",
]


def leer_expresiones_regulares(ruta_archivo="chatbot/expresiones_chatbot_hoteles.csv"):
    patrones = {}
    pesos = {}
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector)  # saltar encabezado
        for intencion, patron, peso in lector:
            patron = patron.strip()
            patrones[intencion.strip()] = re.compile(patron, re.IGNORECASE)
            try:
                pesos[intencion.strip()] = int(peso.strip())
            except:
                pesos[intencion.strip()] = 1
    return patrones, pesos


def calcular_similitud(user_input, patrones, pesos):
    max_peso = 0
    intencion_detectada = None
    for intencion, patron in patrones.items():
        if patron.search(user_input):
            peso = pesos.get(intencion, 1)
            if peso > max_peso:
                max_peso = peso
                intencion_detectada = intencion
    return intencion_detectada, max_peso


def actividades_niños(patrones, pesos):
    print("Hoss: ¿Deseas conocer las opciones de entretenimiento para niños?")
    user_input = input("Tu: ")
    intencion_detectada, max_peso = calcular_similitud(user_input, patrones, pesos)
    if intencion_detectada == "afirmacion":
        print("Hoss: Claro, estas son las actividades:")
        for i in act_niños:
            print(i)
    print("Hoss: ¿En qué más puedo ayudarte?")


def mostrar_comidas(patrones, pesos):
    print("Hoss: ¿Deseas conocer la variedad de comidas que ofrecemos?")
    op = input("Tu: ")
    intencion_detectada, max_peso = calcular_similitud(op, patrones, pesos)
    if intencion_detectada == "afirmacion":
        print(
            "Hoss: Claro, esto es lo que ofrecemos en la comida / cena (pueden variar según la temporada y disponibilidad)."
        )
        print("\n\nDesayunos")
        for i in comidas_op:
            print(i)
        print("\n\nBebidas")
        for i in bebidas_op:
            print(i)
    print("Hoss: ¿En qué más puedo ayudarte?")


def mostrar_bar(patrones, pesos):
    print("Hoss: ¿Deseas conocer las opciones de bebidas con las que contamos?")
    user_input = input("Tu: ")
    intencion_detectada, max_peso = calcular_similitud(user_input, patrones, pesos)
    if intencion_detectada == "afirmacion":
        print(
            "Hoss: Claro, esto es lo que ofrecemos en el bar(pueden variar según la temporada y disponibilidad)."
        )
        print("\n\nBebidas(solo para mayores de edad, todo con medida): ")
        for i in bebidas_alc:
            print(i)
    print("Hoss: ¿En qué más puedo ayudarte?")


def mostrar_desayunos(patrones, pesos):
    user_input = input(
        "¿Deseas conocer las opciones de desayuno con las que contamos? "
    )
    intencion_detectada, max_peso = calcular_similitud(user_input, patrones, pesos)
    if intencion_detectada == "afirmacion":
        print(
            "Hoss: Claro, esto es lo que ofrecemos en el desayuno(pueden variar según la temporada y disponibilidad)."
        )
        print("\n\nDesayunos")
        for i in desayunos_op:
            print(i)
        print("\n\nBebidas: ")
        for i in bebidas_op:
            print(i)
    print("Hoss: ¿En qué más puedo ayudarte?")


def chatbot_hoteles(patrones, pesos):
    contexto = {
        "correo": None,
        "telefono": None,
    }
    print(
        "Hoss: ¡Hola! Soy Hoss, tu asistente virtual para reservas del hostal vaquita marina. ¿En qué puedo ayudarte hoy?"
    )
    while True:
        time.sleep(1)
        user_input = input("Tú: ")

        intencion_detectada, max_peso = calcular_similitud(user_input, patrones, pesos)

        if not user_input.strip():
            print("Hoss: Por favor, ingresa un mensaje válido.")
            continue

        # Responde según la intención detectada
        if intencion_detectada == "salida" or intencion_detectada == "despedida":
            despedidas_respuestas = [
                "Hoss: ¡Adiós! Que tengas un excelente día.",
                "Hoss: ¡Hasta luego! No dudes en contactarme si necesitas ayuda.",
                "Hoss: ¡Fue un placer ayudarte! Que tengas un buen día.",
            ]
            print(random.choice(despedidas_respuestas))
            break
        elif intencion_detectada == "saludo":
            saludos_respuestas = [
                "Hoss: ¡Hola! soy Hoss ¿En qué puedo ayudarte hoy?",
                "Hoss: ¡Saludos! soy Hoss Estoy aquí para asistirte con tus necesidades de hotel.",
                "Hoss: ¡Hola! soy Hoss ¿Buscas reservar una habitación o necesitas información?",
                "Hoss: ¡Bienvenido! ¿Cómo puedo ayudarte con tu estancia?",
                "Hoss: ¡Qué gusto saludarte! ¿En qué te ayudo hoy?",
                "Hoss: ¡Hola! ¿En qué puedo colaborar contigo hoy?",
                "Hoss: ¡Hola! ¿Te gustaría saber sobre nuestras promociones o servicios?",
                "Hoss: ¡Hola! ¿Buscas información sobre habitaciones, precios o servicios?",
                "Hoss: ¡Hola! Soy Hoss, tu asistente virtual. ¿Qué necesitas saber?",
                "Hoss: ¡Hola! ¿En qué puedo orientarte sobre el hostal?",
                "Hoss: ¡Hola! ¿Quieres reservar, cancelar o consultar disponibilidad?",
                "Hoss: ¡Hola! ¿Te ayudo con tu reservación o alguna consulta?",
            ]
            print(random.choice(saludos_respuestas))
            print("Puedes preguntarme sobre:")
            # Solamente ayudara a que se contacten con el usuario
            print("- Reservar una habitación")
            # Solamente ayudara a que se contacten con el usuario
            print("- Cancelar una reservación")
            # Dara informacion tanto de precios de habitaciones como de servicios, y promociones
            print("- Precios y tarifas")
            # Informacion sobre los servicios que ofrece el hotel
            print("- Servicios del hotel")
            # Informacion sobre la accesibilidad del hotel
            print("- Accesibilidad y discapacidades")
            # Informacion sobre la disponibilidad de habitaciones
            print("- Disponibilidad de habitaciones")
            # Informacion sobre la ubicacion del hotel (ficticio)
            print("- Ubicación y cómo llegar")
            # Informacion sobre los horarios de check-in y check-out
            print("- Horarios de check-in y check-out")
            # Informacion sobre las transferencias de pago
            print("- Transferencias de pago")
            continue
        elif intencion_detectada == "reservar":
            print("Hoss: Claro, puedo ayudarte a reservar una habitación.")
            while True:
                print("¿Podrías proporcionarme tu correo electrónico?")
                user_input = input("Tú: ")
                if not user_input.strip():
                    print("Hoss: Por favor, ingresa un mensaje válido.")
                    continue
                patron = patrones.get("validar_correo")
                if not patron.search(user_input):
                    print("Hoss: El correo electrónico proporcionado no es válido. Inténtalo de nuevo.")
                    continue
                contexto["correo"] = user_input.strip()
                break
            while True:
                print("Hoss: Gracias. Ahora, por favor, proporciona tu número de teléfono.")
                user_input = input("Tú: ")
                if not user_input.strip():
                    print("Hoss: Por favor, ingresa un mensaje válido.")
                    continue
                patron = patrones.get("validar_telefono")
                if not patron.search(user_input):
                    print("Hoss: El número de teléfono proporcionado no es válido. Inténtalo de nuevo.")
                    continue
                contexto["telefono"] = user_input.strip()
                break
            print(f"Hoss: Perfecto. He registrado tu correo ({contexto['correo']}) y teléfono ({contexto['telefono']}).\nNos contactaremos con usted para finalizar la reservación.")
            continue
        elif intencion_detectada == "cancelar_reserva":
            cancelar_reserva_respuestas = [
                "Hoss: Para cancelar una reservación, por favor contacta a nuestro equipo de soporte al cliente al correo soporte@hotel.com",
                "Hoss: Si deseas cancelar tu reserva, puedes escribirnos a soporte@hotel.com y te ayudaremos con el proceso.",
                "Hoss: Para cancelar, envía un correo a soporte@hotel.com y nuestro equipo te asistirá.",
                "Hoss: Puedes cancelar tu reservación contactando a soporte@hotel.com. ¿Necesitas ayuda adicional?",
            ]
            print(random.choice(cancelar_reserva_respuestas))
            continue
        elif intencion_detectada == "precio":
            precio_respuestas = [
                "Hoss: Ofrecemos descuentos especiales para reservas anticipadas y estancias prolongadas. ¿Te gustaría saber más?",
                "Hoss: Los precios de las habitaciones comienzan desde $100 por noche. ¿Quieres información sobre algún tipo de habitación en particular?",
                "Hoss: El precio depende del tipo de habitación y la temporada. ¿Te gustaría saber los precios de habitaciones sencillas, dobles o suites?",
                "Hoss: Tenemos tarifas flexibles según la duración de la estancia y el número de personas. ¿Te gustaría una cotización personalizada?",
                "Hoss: Puedes consultar nuestras tarifas y promociones en el sitio web o preguntarme directamente por el tipo de habitación que te interesa.",
                "Hoss: ¿Buscas precios para una fecha específica o para algún tipo de habitación en particular?",
                "Hoss: Si reservas con más de 30 días de anticipación, obtienes un 20% de descuento. ¿Te gustaría aprovecharlo?",
                "Hoss: ¿Quieres saber el precio por noche, por semana o por mes?",
                "Hoss: ¿Te gustaría saber el precio para una persona, pareja o grupo?",
            ]
            print(random.choice(precio_respuestas))
            user_input = input("Tú: ")
            if not user_input.strip():
                print("Hoss: Por favor, ingresa un mensaje válido.")
                continue
            patron = patrones.get("afirmacion")
            if patron.search(user_input):
                print(
                    "Hoss: Actualmente tenemos una promoción del 20% de descuento para reservas realizadas con al menos 30 días de anticipación."
                )
                print("Hoss: La habitación sencilla cuesta $100 por noche.")
                print("Hoss: La habitación doble cuesta $150 por noche.")
                print("Hoss: La suite cuesta $250 por noche.")
                continue
        elif intencion_detectada == "promocion":
            promocion_respuestas = [
                "Hoss: Actualmente tenemos una promoción del 20% de descuento para reservas realizadas con al menos 30 días de anticipación.",
                "Hoss: Si reservas con más de 30 días de anticipación, obtienes un 20% de descuento en tu estancia.",
                "Hoss: ¡Aprovecha nuestra promoción! 20% de descuento en reservas anticipadas.",
                "Hoss: Tenemos una oferta especial: 20% de descuento si reservas con al menos 30 días de anticipación.",
                "Hoss: ¿Te gustaría aprovechar el 20% de descuento por reservar con anticipación?",
                "Hoss: Reserva con tiempo y obtén un 20% de descuento en cualquier tipo de habitación.",
                "Hoss: Nuestra promoción vigente es 20% de descuento para reservas anticipadas. ¿Te interesa?",
                "Hoss: Si planeas tu viaje con tiempo, puedes obtener un 20% de descuento en tu reservación.",
            ]
            print(random.choice(promocion_respuestas))
            continue
        elif intencion_detectada == "tipo_habitacion_sencilla":
            sencilla_respuestas = [
                "Hoss: La habitación sencilla cuesta $100 por noche.",
                "Hoss: El precio de la habitación sencilla es de $100 por noche, ideal para una persona.",
                "Hoss: Si buscas privacidad, la habitación sencilla está disponible por $100 la noche.",
                "Hoss: La opción sencilla cuesta $100 por noche e incluye desayuno y Wi-Fi.",
            ]
            sencilla_incluye = [
                "Hoss: La habitación sencilla incluye una cama individual, baño privado, Wi-Fi gratuito, televisión por cable, aire acondicionado y desayuno continental.",
                "Hoss: Al reservar la sencilla tienes acceso a Wi-Fi, desayuno continental, aire acondicionado, TV por cable y baño privado.",
                "Hoss: La opción sencilla te ofrece cama individual, baño privado, desayuno incluido, Wi-Fi y aire acondicionado.",
                "Hoss: La habitación sencilla cuenta con cama individual, baño privado, Wi-Fi gratis, TV por cable y desayuno continental.",
                "Hoss: Incluye cama individual, baño privado, Wi-Fi, aire acondicionado, TV por cable y desayuno continental.",
                "Hoss: Disfruta de baño privado, Wi-Fi, desayuno continental, aire acondicionado y TV por cable en la sencilla.",
                "Hoss: La sencilla incluye desayuno, Wi-Fi, aire acondicionado, baño privado y televisión por cable.",
            ]
            print(random.choice(sencilla_respuestas))
            print(random.choice(sencilla_incluye))
            continue
        elif intencion_detectada == "tipo_habitacion_doble":
            doble_respuestas = [
                "Hoss: La habitación doble cuesta $150 por noche.",
                "Hoss: El precio de la habitación doble es de $150 por noche, perfecta para parejas o amigos.",
                "Hoss: Si viajas acompañado, la habitación doble está disponible por $150 la noche.",
                "Hoss: La opción doble cuesta $150 por noche e incluye desayuno y Wi-Fi.",
            ]
            doble_incluye = [
                "Hoss: La habitación doble incluye dos camas individuales o una cama matrimonial, baño privado, Wi-Fi gratuito, televisión por cable, aire acondicionado y desayuno buffet.",
                "Hoss: Al reservar la doble tienes acceso a Wi-Fi, desayuno buffet, aire acondicionado, TV por cable y baño privado.",
                "Hoss: La opción doble te ofrece dos camas o cama matrimonial, baño privado, desayuno incluido, Wi-Fi y aire acondicionado.",
                "Hoss: La habitación doble cuenta con baño privado, Wi-Fi gratis, TV por cable y desayuno buffet.",
                "Hoss: Incluye dos camas o cama matrimonial, baño privado, Wi-Fi, aire acondicionado, TV por cable y desayuno buffet.",
                "Hoss: Disfruta de baño privado, Wi-Fi, desayuno buffet, aire acondicionado y TV por cable en la doble.",
                "Hoss: La doble incluye desayuno buffet, Wi-Fi, aire acondicionado, baño privado y televisión por cable.",
            ]
            print(random.choice(doble_respuestas))
            print(random.choice(doble_incluye))
            continue
        elif intencion_detectada == "tipo_habitacion_suite":
            suite_respuestas = [
                "Hoss: La suite cuesta $250 por noche.",
                "Hoss: El precio de la suite es de $250 por noche, ideal para quienes buscan lujo y comodidad.",
                "Hoss: Si quieres una experiencia premium, la suite está disponible por $250 la noche.",
                "Hoss: La suite cuesta $250 por noche e incluye desayuno, Wi-Fi y acceso al spa.",
            ]
            suite_incluye = [
                "Hoss: La suite incluye cama king size, sala de estar, baño privado con tina, Wi-Fi gratuito, televisión por cable, aire acondicionado, desayuno buffet y acceso al spa.",
                "Hoss: Al reservar la suite tienes acceso a Wi-Fi, desayuno buffet, aire acondicionado, TV por cable, baño privado con tina y spa.",
                "Hoss: La opción suite te ofrece cama king size, sala, baño privado con tina, desayuno incluido, Wi-Fi y aire acondicionado.",
                "Hoss: La suite cuenta con sala de estar, baño privado con tina, Wi-Fi gratis, TV por cable y desayuno buffet.",
                "Hoss: Incluye cama king size, sala, baño privado con tina, Wi-Fi, aire acondicionado, TV por cable, desayuno buffet y spa.",
                "Hoss: Disfruta de sala de estar, baño privado con tina, Wi-Fi, desayuno buffet, aire acondicionado y TV por cable en la suite.",
                "Hoss: La suite incluye desayuno buffet, Wi-Fi, aire acondicionado, baño privado con tina, televisión por cable y acceso al spa.",
            ]
            print(random.choice(suite_respuestas))
            print(random.choice(suite_incluye))
            continue
        elif intencion_detectada == "cant_max_personas":
            max_personas_respuestas = [
                "Hoss: La habitación sencilla es para 1 persona, la doble para 2 personas y la suite para hasta 4 personas.",
                "Hoss: La capacidad máxima es 1 persona en sencilla, 2 en doble y 4 en suite.",
                "Hoss: Puedes alojar a 1 persona en una sencilla, 2 en una doble y hasta 4 en una suite.",
                "Hoss: La habitación sencilla es individual, la doble es para parejas o amigos, y la suite puede acomodar a familias pequeñas.",
            ]
            print(random.choice(max_personas_respuestas))
            continue
        elif intencion_detectada == "servicios":
            servicios_respuestas = [
                "Hoss: Nuestro hotel ofrece accesibilidad para discapacitados, Wi-Fi gratuito, desayuno incluido, spa, gimnasio, piscina, restaurante, bar, parking, servicio de habitaciones 24 horas y espacios para niños.",
                "Hoss: Contamos con servicios como acceso a discapacitados, Wi-Fi, desayuno, spa, gimnasio, piscina, restaurante, bar, estacionamiento gratuito y espacios para niños.",
                "Hoss: Puedes disfrutar de Wi-Fi, desayuno buffet, spa, gimnasio, piscina, restaurante, bar, parking y espacios para niños sin costo adicional.",
                "Hoss: Ofrecemos accesibilidad para discapacitados,Wi-Fi, desayuno, spa, gimnasio, piscina, restaurante, bar, parking, servicio de habitaciones todo el día y espacios para niños.",
            ]
            print(random.choice(servicios_respuestas))
            continue
        elif intencion_detectada == "niños":
            niños_respuestas = [
                "Hoss: Sí, nuestro hotel es apto para niños. Contamos con habitaciones familiares y áreas de juego para que los más pequeños se diviertan.",
                "Hoss: Claro, tenemos facilidades para niños, incluyendo habitaciones familiares y actividades recreativas.",
                "Hoss: Los niños son bienvenidos en nuestro hotel. Ofrecemos habitaciones adaptadas y zonas de juegos.",
                "Hoss: Sí, puedes hospedarte con tus hijos. Tenemos servicios y espacios diseñados para familias.",
            ]
            print(random.choice(niños_respuestas))
            actividades_niños(patrones, pesos)
            continue
        elif intencion_detectada == "wifi":
            wifi_respuestas = [
                "Hoss: Sí, tenemos Wi-Fi gratuito en todo el hotel. De una velocidad de bajada de 20 Mbps y de subida de 10 Mbps.",
                "Hoss: El hotel cuenta con Wi-Fi gratis en todas las áreas, ideal para trabajar o entretenerte.",
                "Hoss: Puedes conectarte a nuestro Wi-Fi sin costo en habitaciones y áreas comunes.",
                "Hoss: La conexión Wi-Fi es rápida y estable, disponible para todos los huéspedes.",
            ]
            print(random.choice(wifi_respuestas))
            continue
        elif intencion_detectada == "mascotas":
            mascotas_respuestas = [
                "Hoss: Sí, puedes ingresar con mascotas o animales de servicio tales como perros lazarillo ó animales de soporte emocional.",
                "Hoss: Admitimos mascotas y animales de servicio. ¿Viajas con algún compañero peludo?",
                "Hoss: Tu mascota es bienvenida en nuestro hotel. Solo avísanos al momento de reservar.",
                "Hoss: Somos pet friendly, así que puedes hospedarte con tu mascota sin problema.",
            ]
            print(random.choice(mascotas_respuestas))
            continue
        elif intencion_detectada == "accesibilidad":
            accesibilidad_respuestas = [
                "Hoss: Sí, contamos con espacios accesibles para personas con capacidades diferentes. Tenemos rampas, ascensores y habitaciones adaptadas.",
                "Hoss: El hotel está adaptado para personas con movilidad reducida, con rampas y elevadores.",
                "Hoss: Disponemos de habitaciones accesibles y facilidades para personas con discapacidad.",
                "Hoss: Si necesitas accesibilidad, tenemos instalaciones adaptadas para tu comodidad.",
            ]
            print(random.choice(accesibilidad_respuestas))
            continue
        elif intencion_detectada == "desayuno":
            desayuno_respuestas = [
                "Hoss: Sí, el desayuno está incluido en la tarifa de la habitación y se sirve de 7:00 a 10:30 AM en el restaurante del hotel.",
                "Hoss: El desayuno buffet está disponible para todos los huéspedes de 7:00 a 10:30 AM.",
                "Hoss: Puedes disfrutar de desayuno continental incluido en tu estancia.",
                "Hoss: El desayuno es gratis y se sirve en el restaurante cada mañana.",
            ]
            print(random.choice(desayuno_respuestas))
            mostrar_desayunos(patrones, pesos)
            continue
        elif intencion_detectada == "spa":
            spa_respuestas = [
                "Hoss: Sí, contamos con un spa que ofrece masajes, tratamientos faciales y corporales. Está abierto de 9:00 AM a 9:00 PM.",
                "Hoss: El spa está disponible para todos los huéspedes, con masajes y tratamientos relajantes.",
                "Hoss: Puedes reservar un masaje o tratamiento en nuestro spa de 9:00 AM a 9:00 PM.",
                "Hoss: El spa ofrece servicios de relajación y belleza para tu bienestar.",
            ]
            print(random.choice(spa_respuestas))
            continue
        elif intencion_detectada == "gimnasio":
            gimnasio_respuestas = [
                "Hoss: Sí, contamos con un gimnasio equipado con máquinas de cardio y pesas. Está abierto las 24 horas.",
                "Hoss: Sí, hay gimnasio disponible todo el día para que entrenes cuando quieras.",
                "Hoss: Sí, puedes usar el gimnasio con equipos modernos y área de pesas durante tu estancia.",
                "Hoss: Sí, el acceso al gimnasio está incluido en tu estancia, abierto 24/7.",
                "Hoss: Sí, tenemos gimnasio para todos los huéspedes, abierto las 24 horas.",
                "Hoss: Sí, el hotel cuenta con gimnasio equipado y disponible en cualquier momento.",
            ]
            print(random.choice(gimnasio_respuestas))
            continue
        elif intencion_detectada == "piscina":
            piscina_respuestas = [
                "Hoss: Sí, tenemos una piscina al aire libre disponible para nuestros huéspedes. Está abierta de 8:00 AM a 10:00 PM.",
                "Hoss: La piscina está abierta todos los días de 8:00 AM a 10:00 PM para tu diversión.",
                "Hoss: Puedes disfrutar de la piscina climatizada durante tu estancia.",
                "Hoss: La alberca está disponible para relajarte y nadar cuando gustes.",
            ]
            print(random.choice(piscina_respuestas))
            continue
        elif intencion_detectada == "ubicacion":
            ubicacion_respuestas = [
                "Hoss: Se encuentra en Calz. de Tlalpan 663, Álamos, Benito Juárez, 03400 Ciudad de México, CDMX.",
                "Hoss: La dirección es Calz. de Tlalpan 663, Col. Álamos, Benito Juárez, CDMX.",
                "Hoss: Estamos ubicados en la zona sur de la Ciudad de México, cerca del metro Xola.",
                "Hoss: Puedes encontrarnos en Calz. de Tlalpan 663, a unos pasos del metro Xola.",
            ]
            como_llegar_respuestas = [
                "Hoss: Para llegar puedes tomar el metro Xola y caminar hacia el sur.",
                "Hoss: La mejor ruta es llegar al metro Xola y caminar en dirección sur.",
                "Hoss: Puedes llegar fácilmente desde el metro Xola, estamos a pocos minutos caminando.",
                "Hoss: Desde el metro Xola, camina hacia el sur y nos encontrarás pronto.",
            ]
            print(random.choice(ubicacion_respuestas))
            print(random.choice(como_llegar_respuestas))
            continue
        elif intencion_detectada == "bar":
            bar_respuestas = [
                "Hoss: Sí, contamos con un  bar que ofrece una variedad de bebidas locales e internacionales. Está abierto de 12:00 PM a 12:00 AM.",
                "Hoss: El restaurante y bar está abierto de 12:00 PM a 12:00 AM, con menú variado y bebidas.",
                "Hoss: Puedes disfrutar de platillos locales e internacionales en nuestro bar.",
                "Hoss: El bar ofrece cocteles y bebidas especiales, abierto hasta las 12:00 AM.",
            ]
            print(random.choice(bar_respuestas))
            mostrar_bar(patrones, pesos)
            continue
        elif intencion_detectada == "comida":
            comida_respuestas = [
                "Hoss: Sí, contamos con un restaurante que ofrece una variedad de platos y bebidas locales e internacionales. Está abierto de 12:00 PM a 12:00 AM.",
                "Hoss: El restaurante y bar está abierto de 12:00 PM a 12:00 AM, con menú variado y bebidas.",
                "Hoss: Puedes disfrutar de platillos locales e internacionales en nuestro restaurante.",
                "Hoss: El restaurante ofrece una gran variedad de comidas y platillos.",
            ]
            print(random.choice(comida_respuestas))
            mostrar_comidas(patrones, pesos)
            continue
        elif intencion_detectada == "parking":
            parking_respuestas = [
                "Hoss: Sí, ofrecemos estacionamiento gratuito para nuestros huéspedes. No es necesario reservar con anticipación.",
                "Hoss: El parking es gratis y está disponible para todos los huéspedes.",
                "Hoss: Puedes estacionar tu auto sin costo adicional, no necesitas reservar.",
                "Hoss: El hotel cuenta con estacionamiento privado y seguro para tu comodidad.",
            ]
            print(random.choice(parking_respuestas))
            continue
        elif intencion_detectada == "servicio_habitaciones":
            servicio_habitaciones_respuestas = [
                "Hoss: Sí, ofrecemos servicio de habitaciones las 24 horas. Puedes pedir desde el menú del restaurante directamente a tu habitación.",
                "Hoss: El servicio de habitaciones está disponible todo el día para tu comodidad.",
                "Hoss: Puedes solicitar comida, bebidas o limpieza a tu habitación en cualquier momento.",
                "Hoss: Nuestro servicio de habitaciones es rápido y eficiente, disponible las 24 horas.",
            ]
            print(random.choice(servicio_habitaciones_respuestas))
            continue
        elif intencion_detectada == "disponibilidad":
            disponibilidad_respuestas = [
                "Hoss: Para verificar la disponibilidad de habitaciones, por favor visita nuestro sitio web o contacta a nuestro equipo de soporte al cliente al correo electrónico soporte@hotel.com.",
                "Hoss: Puedes consultar la disponibilidad en línea o escribiendo a soporte@hotel.com.",
                "Hoss: Para saber si hay habitaciones disponibles, revisa nuestro sitio web o contáctanos por correo.",
                "Hoss: La disponibilidad de habitaciones se puede consultar en nuestro sitio web o por correo electrónico.",
            ]
            print(random.choice(disponibilidad_respuestas))
            continue
        elif intencion_detectada == "checkin_checkout":
            checkin_checkout_respuestas = [
                "Hoss: El horario de check-in es a partir de las 3:00 PM y el check-out es hasta las 12:00 PM.",
                "Hoss: Puedes ingresar al hotel desde las 3:00 PM y salir hasta las 12:00 PM.",
                "Hoss: El check-in comienza a las 3:00 PM y el check-out es antes de las 12:00 PM.",
                "Hoss: El horario de entrada es 3:00 PM y la salida es a las 12:00 PM.",
            ]
            print(random.choice(checkin_checkout_respuestas))
            continue
        elif intencion_detectada == "metodo_pago":
            metodo_pago_respuestas = [
                "Hoss: Aceptamos tarjetas de crédito y débito, transferencias bancarias y pagos en efectivo. Para reservas en línea, aceptamos PayPal y Stripe.",
                "Hoss: Puedes pagar con tarjeta, transferencia, efectivo, PayPal o Stripe según tu preferencia.",
                "Hoss: Ofrecemos varias opciones de pago: tarjeta, transferencia, efectivo y plataformas digitales.",
                "Hoss: El pago puede hacerse en línea o en el hotel, según lo que te convenga.",
            ]
            efectivo_respuestas = [
                "Hoss: En caso de que quieras pagar en efectivo, puedes hacerlo al momento del check-in o check-out.",
                "Hoss: El pago en efectivo se realiza directamente en la recepción al ingresar o salir.",
                "Hoss: Si prefieres pagar en efectivo, puedes hacerlo al llegar o al salir del hotel.",
                "Hoss: El pago en efectivo está disponible en el check-in y check-out.",
            ]
            print(random.choice(metodo_pago_respuestas))
            print(random.choice(efectivo_respuestas))
            continue
        elif intencion_detectada == "easter_egg":
            easter_egg_respuestas = [
                "Hoss: ¡Eres digno de encontrar el One Piece! ¿Te gustaría navegar por la Grand Line conmigo?",
                "Hoss: ¡Has desbloqueado el Gear 5! Ahora eres tan fuerte como Luffy.",
                "Hoss: ¡Bienvenido a la tripulación de los Sombrero de Paja! ¿Prefieres ser navegante como Nami o espadachín como Zoro?",
                "Hoss: ¡El tesoro de Gol D. Roger está más cerca de lo que crees! Sigue buscando pistas.",
                "Hoss: ¡Shanks estaría orgulloso de tu espíritu aventurero!",
                "Hoss: ¡Has encontrado el Sunny! ¿Listo para zarpar hacia el Nuevo Mundo?",
                "Hoss: ¡Solo los verdaderos piratas encuentran este mensaje! ¿Te gustaría una Akuma no Mi?",
                "Hoss: ¡Impel Down no puede detenerte! Sigue explorando el mundo de One Piece.",
                "Hoss: ¡La era de los piratas ha comenzado! ¿Cuál es tu sueño en el mar?",
                "Hoss: ¡Brook te saluda desde el otro mundo! Yohohoho~",
                "Hoss: ¡Sanji te preparará el mejor banquete en el Baratie!",
                "Hoss: ¡Zoro te reta a un duelo de espadas!",
                "Hoss: ¡Nami te ayudará a encontrar el tesoro!",
                "Hoss: ¡Usopp te contará una historia increíble!",
                "Hoss: ¡Robin te enseñará la historia perdida del mundo!",
                "Hoss: ¡Franky dice: SUPER! por tu descubrimiento.",
                "Hoss: ¡Jinbe te invita a nadar con los hombres pez!",
            ]
            print(random.choice(easter_egg_respuestas))
            continue
        elif intencion_detectada == "correo" or intencion_detectada == "telefono":
            contacto_respuestas = [
                "Hoss: Si necesitas contactarte o comunicarte con nosotros, puedes escribir a: soporte@hotel.com o llamar al (55) 1234-5678.",
                "Hoss: Nuestro correo de contacto es soporte@hotel.com y el teléfono es (55) 1234-5678.",
                "Hoss: Puedes enviarnos un correo a soporte@hotel.com o llamarnos al (55) 1234-5678 para cualquier consulta.",
                "Hoss: Para comunicarte con el hotel, utiliza el correo soporte@hotel.com o el teléfono (55) 1234-5678.",
                "Hoss: Si tienes dudas, escríbenos a soporte@hotel.com o marca al (55) 1234-5678.",
                "Hoss: Nuestro equipo te atenderá en soporte@hotel.com o al teléfono (55) 1234-5678.",
                "Hoss: ¿Necesitas ayuda? Contáctanos por correo (soporte@hotel.com) o por teléfono ((55) 1234-5678).",
                "Hoss: Para atención personalizada, comunícate al correo soporte@hotel.com o al teléfono (55) 1234-5678.",
            ]
            print(random.choice(contacto_respuestas))
            continue
        else:
            respuestas_default = [
                "Hoss: Lo siento, no entendí tu solicitud. Por favor, proporciona más detalles o especifica tu pregunta.",
                "Hoss: No estoy seguro de cómo ayudarte con eso. Intenta describir lo que necesitas de otra forma.",
                "Hoss: No entiendo tu pregunta. Puedes darme más información o contexto para poder ayudarte mejor.",
                "Hoss: Disculpa, no logré captar lo que necesitas. Por favor, explica tu solicitud con más detalle.",
                "Hoss: No tengo información suficiente para responderte. Especifica el tema o el tipo de información que buscas.",
                "Hoss: No encontré una respuesta para tu consulta. Reformula tu pregunta o indica el área de interés (habitaciones, servicios, ubicación, etc.).",
                "Hoss: Mi base de datos no tiene esa información. Si tienes otra consulta específica, por favor escríbela.",
                "Hoss: No estoy seguro de haber entendido. Proporciona más contexto o detalles sobre lo que necesitas.",
                "Hoss: Perdón, no tengo una respuesta clara para eso. Intenta explicar tu solicitud con mayor precisión.",
                "Hoss: No tengo la respuesta en este momento. Si buscas información sobre habitaciones, servicios, ubicación o precios, indícalo directamente.",
                "Hoss: No logré identificar tu intención. Reformula tu pregunta para poder ayudarte mejor.",
                "Hoss: No tengo información sobre eso. Especifica el tema de tu consulta para poder asistirte.",
            ]
            print(random.choice(respuestas_default))
            continue

        mas_ayuda_respuestas = [
            "Hoss: ¿En qué más puedo ayudarte?",
            "Hoss: ¿Te gustaría saber algo más sobre el hotel?",
            "Hoss: ¿Hay otra consulta que quieras hacer?",
            "Hoss: ¿Puedo ayudarte con otra información?",
            "Hoss: ¿Necesitas saber algo más?",
            "Hoss: ¿Tienes otra pregunta o duda?",
            "Hoss: ¿Te ayudo con otra cosa?",
            "Hoss: ¿Quieres preguntar sobre habitaciones, servicios o promociones?",
            "Hoss: ¿Te gustaría conocer más detalles del hotel?",
            "Hoss: ¿En qué más te puedo asistir?",
        ]
        print(random.choice(mas_ayuda_respuestas))


if __name__ == "__main__":
    patrones, pesos = leer_expresiones_regulares()
    chatbot_hoteles(patrones, pesos)
