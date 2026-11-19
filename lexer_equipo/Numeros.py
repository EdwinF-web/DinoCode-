import re  # Biblioteca estándar de Python para trabajar con expresiones regulares

# Lista de tuplas con los patrones de los tokens que este módulo reconoce.
# El orden importa: "decimal" debe ir antes que "entero" para que no corte el número en el punto.
tipos = [
    # Busca uno o más dígitos (\d+), seguidos de un punto literal (\.), y uno o más dígitos (\d+)
    ("decimal", re.compile(r"\d+\.\d+")),
    # Busca uno o más dígitos seguidos [0-9]
    ("entero", re.compile(r"\d+")),
    # \b indica límite de palabra (evita que detecte "cierto" dentro de "incierto").
    # (?:...) agrupa las opciones válidas en español (minúsculas, mayúsculas o capitalizadas).
    ("boleano", re.compile(r"\b(?:cierto|falso|FALSO|CIERTO|Cierto|Falso)\b")),
]


def idennum(palabra, posic=0):
    """
    Intenta identificar un token (decimal, entero o booleano) a partir de una posición exacta.
    Parámetros:
      - palabra: la cadena de texto completa que se está analizando.
      - posic: el índice desde donde empieza a buscar (por defecto 0).
    """
    # Recorre cada par (nombre_del_tipo, expresion_regular_compilada)
    for nom, expre in tipos:
        # match() comprueba si el patrón coincide exactamente a partir de 'posic'
        a = expre.match(palabra, posic)
        if a:
            # Si hubo coincidencia, devuelve:
            # 1. nom: el tipo de token ("decimal", "entero" o "boleano")
            # 2. a.group(): el texto exacto encontrado (ej. "45.8" o "Cierto")
            # 3. a.end(): la posición donde terminó el token para saber dónde seguir leyendo
            return nom, a.group(), a.end()

    # Si terminó el ciclo y ningún patrón coincidió en esa posición, devuelve None
    return None


def analizar_numeros(palabra):
    """
    Recorre toda una cadena de texto de principio a fin y extrae todos los tokens válidos.
    Devuelve una lista de tuplas (tipo, valor) o None si encuentra un carácter no reconocido.
    """
    posi = 0  # Puntero o índice que indica qué carácter estamos leyendo actualmente
    tokens_encontrados = []  # Lista vacía donde se irán guardando los tokens válidos

    # El ciclo se repite mientras no lleguemos al final del texto
    while posi < len(palabra):
        # Si el carácter actual es un espacio en blanco, tabulación o salto de línea
        if palabra[posi].isspace():
            posi += 1  # Avanzamos el puntero una posición para ignorar el espacio
            continue  # Saltamos directamente a la siguiente vuelta del ciclo while

        # Llamamos a idennum para ver si en la posición actual empieza un número o booleano
        token = idennum(palabra, posi)

        # Si token es None, significa que hay un símbolo o palabra que este módulo no reconoce
        if token is None:
            print(f"Error léxico en la posición {posi}: '{palabra[posi]}'")
            return None  # Detiene el análisis y avisa que hubo un error

        # Desempaquetamos la tupla devuelta por idennum en tres variables:
        # 'tip' guarda el tipo, 'valor' el texto, y 'posi' se actualiza a la nueva posición
        tip, valor, posi = token

        # Guardamos el par (tipo, valor) en nuestra lista de resultados
        tokens_encontrados.append((tip, valor))

    # Cuando termina de leer todo el texto sin errores, devuelve la lista completa de tokens
    return tokens_encontrados
