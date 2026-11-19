#reconocer operadores, símbolos y comentarios


OPERADORES = {
    #asignacion
    "<-": "ASIGNA",
    "=": "ASIGNA_CONSTANTE",
    #aritmeticos
    "+": "SUMA",
    "-": "RESTA",
    "*": "MULTIPLICACION",
    "/": "DIVISION",
    "%": "MODULO",
    #comparacion
    "==": "IGUAL",
    "!=": "DIFERENTE",
    "<": "MENOR_QUE",
    ">": "MAYOR_QUE",
    "<=": "MENOR_IGUAL",
    ">=": "MAYOR_IGUAL",
    #concatenacion
    "#": "CONCATENA",
    #parentesis
    "(": "PAREN_IZQ",
    ")": "PAREN_DER",
    #logicos
    "y": "Y",
    "o": "O",
}

def reconocer_comentario(codigo, posicion):
    #reconoce comentarios 

    if codigo.startswith("d<", posicion):

        fin = codigo.find(">d", posicion + 2)

        if fin == -1:
            return {
                "tipo": "ERROR_COMENTARIO_SIN_CERRAR",
                "valor": codigo[posicion:],
                "longitud": len(codigo) - posicion
            }
        fin += 2

        texto = codigo[posicion:fin]

        return {
            "tipo": "COMENTARIO",
            "valor": texto,
            "longitud": len(texto)
        }

    return None


def reconocer_operador(codigo, posicion):
    #identifica operadores y simbolos

    # primero revisar si es un comentario
    comentario = reconocer_comentario(codigo, posicion)

    if comentario is not None:
        return comentario

    #se ordena para reconocer primero los simbolos de dos caracteres ()>=, <=, <-, ==)
    for simbolo in sorted(OPERADORES, key=len, reverse=True):

        if codigo.startswith(simbolo, posicion):

            #verifica cuando sea un operador de palabra
            if simbolo.isalpha():

                anterior = codigo[posicion - 1] if posicion > 0 else ""
                siguiente_pos = posicion + len(simbolo)
                siguiente = codigo[siguiente_pos] if siguiente_pos < len(codigo) else ""

                if (anterior.isalnum() or anterior == "_") or \
                   (siguiente.isalnum() or siguiente == "_"):
                    continue

            return {
                "tipo": OPERADORES[simbolo],
                "valor": simbolo,
                "longitud": len(simbolo)
            }

    return None