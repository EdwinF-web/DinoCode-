# =============================================================================
# DINOCODE - ANALIZADOR LÉXICO (LEXER) v1.1
# =============================================================================
# Este archivo reemplaza a: lexerCerregido7.py, Cadenas.py, Numeros.py,
# operadores.py, ErroresLexicos.py y ValidacionesLexicas.py
#
# Decisiones congeladas:
#   - Comentarios: d> abre; <d cierra; sin <d en la línea -> hasta \n
#   - Palabras reservadas: minúsculas, MAYÚSCULAS o Primera_mayúscula.
#     La forma mixta arbitraria (hUeVo) NO es válida.
#   - Forma canónica: si_ve, no_ve, o_ve, fin_si, fin_caza (guion bajo)
#   - captura (no capturar), verdadero/falso (no cierto/falso)
#   - Sin punto y coma (;)
#   - rugir acepta con o sin paréntesis
#   - : obligatorio tras haz y tras avanzar ...
#   - i++ y i <- i + 1 ambos válidos
#   - Solo comillas dobles para cadenas
#   - Identificadores con tilde/ñ permitidos
#   - Token EOF al final
#   - Errores acumulados en AdministradorErrores (no SyntaxError)
# =============================================================================

import re



# 1. PALABRAS RESERVADAS
# Se comparan en minúsculas, por eso el set está todo en minúsculas.
# Al leer un identificador, se normaliza con .lower() y se busca aquí.

PALABRAS_RESERVADAS = { #set donde se almacena las palabras reservadas 
    "huevo", "captura", "rugir",
    "si_ve", "no_ve", "o_ve",
    "haz", "fin_si",
    "cazar", "desde", "hasta", "avanzar", "fin_caza",
    "verdadero", "falso",
}



# 2. OPERADORES Y SÍMBOLOS
# El orden de evaluación es CRÍTICO: siempre se ordenan por longitud
# descendente antes de comparar, para que "++" gane a "+", "==" gane a "=",
# "<-" gane a "<", etc.


OPERADORES = {
    # Asignación
    "<-": "ASIGNA",
    "=":  "ASIGNA_CONSTANTE",
    # Incremento (debe evaluarse antes que "+")
    "++": "INCREMENTO",
    # Aritméticos
    "+":  "SUMA",
    "-":  "RESTA",
    "*":  "MULTIPLICACION",
    "/":  "DIVISION",
    "%":  "MODULO",
    # Comparación
    "==": "IGUAL",
    "!=": "DIFERENTE",
    "<":  "MENOR_QUE",
    ">":  "MAYOR_QUE",
    "<=": "MENOR_IGUAL",
    ">=": "MAYOR_IGUAL",
    # Concatenación
    "#":  "CONCATENA",
}

# Operadores de palabra (se evalúan aparte porque requieren límites de palabra)
OPERADORES_PALABRA = {
    "y": "Y",
    "o": "O",
}

# Símbolos de un solo carácter que no son operadores
SIMBOLOS = {
    "(": "PAREN_IZQ",
    ")": "PAREN_DER",
    ":": "DOS_PUNTOS",
    ",": "COMA",
}



# 3. GESTIÓN DE ERRORES LÉXICOS

# En vez de lanzar SyntaxError (que aborta), acumulamos errores con
# línea y columna para reportarlos todos al final.


class ErrorLexico:
   # Representa un error léxico con posición.

    def __init__(self, mensaje, linea, columna, fragmento):
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna
        self.fragmento = fragmento

    def __str__(self):
        return (f"Error léxico: {self.mensaje} "
                f"'{self.fragmento}' en línea {self.linea}, columna {self.columna}")


class AdministradorErrores:
    #Acumula errores léxicos durante el análisis.

    def __init__(self):
        self.errores = []

    def agregar(self, mensaje, linea, columna, fragmento):
        self.errores.append(ErrorLexico(mensaje, linea, columna, fragmento))

    def tiene_errores(self):
        return len(self.errores) > 0

    def cantidad(self):
        return len(self.errores)

    def mostrar(self):
        if not self.errores:
            print("No se encontraron errores léxicos.")
            return
        print("\n========== ERRORES DINOCODE ==========")
        for i, e in enumerate(self.errores, start=1):
            print(f"{i}. {e}")
        print("======================================")



# 4. CREACIÓN DE TOKENS
# Formato único de token: dict con tipo, valor, línea y columna.


def crear_token(tipo, valor, linea, columna):
    return {
        "tipo": tipo,
        "valor": valor,
        "linea": linea,
        "columna": columna,
    }


# 5. LECTURA DE COMENTARIOS
# Regla: d> abre; <d cierra; si no hay <d en la MISMA línea, corta en \n.
# Se ignoran silenciosamente (no emiten token).


def leer_comentario(codigo, posicion):
    
    #Recibe la posición justo después de 'd>'.
    #Devuelve la nueva posición (fin del comentario).
    
    # Buscar el próximo salto de línea
    salto = codigo.find("\n", posicion)
    fin_linea = salto if salto != -1 else len(codigo)

    # Buscar <d SOLO dentro de esta línea
    cierre = codigo.find("<d", posicion, fin_linea)

    if cierre != -1:
        # Comentario cerrado con <d en la misma línea
        return cierre + 2

    # Sin <d: comentario unilínea, corta en \n (o fin de archivo)
    return fin_linea


# =============================================================================
# 6. LECTURA DE NÚMEROS
# =============================================================================
# Acepta enteros (42) y decimales (3.1416).
# Rechaza 5. y .5 (el punto debe tener dígitos a ambos lados).
# =============================================================================

def leer_numero(codigo, posicion):
    #Devuelve (valor_texto, nueva_posicion).
    inicio = posicion

    # Parte entera
    while posicion < len(codigo) and codigo[posicion].isdigit():
        posicion += 1

    # Parte decimal (solo si hay dígitos después del punto)
    if (posicion < len(codigo)
            and codigo[posicion] == "."
            and posicion + 1 < len(codigo)
            and codigo[posicion + 1].isdigit()):
        posicion += 1
        while posicion < len(codigo) and codigo[posicion].isdigit():
            posicion += 1

    return codigo[inicio:posicion], posicion



# 7. VALIDACIÓN DE FORMA DE PALABRA RESERVADA
# Solo se aceptan tres formas:
#   - todo minúsculas:      huevo, si_ve, fin_caza
#   - todo mayúsculas:      HUEVO, SI_VE, FIN_CAZA
#   - primera mayúscula:    Huevo, Si_ve, Fin_caza
# La forma mixta arbitraria (hUeVo, fIn_CaZa, SI_vE) NO es válida.


def forma_valida(texto):
    """True si el texto cumple una de las tres formas aceptadas."""
    return (texto.islower()
            or texto.isupper()
            or (texto[0].isupper() and texto[1:].islower()))



# 8. LECTURA DE IDENTIFICADORES Y PALABRAS RESERVADAS
# - Identificador: letra o _ seguido de letras/dígitos/_ (acepta tildes y ñ).
# - Si el texto (en minúsculas) está en PALABRAS_RESERVADAS Y su forma es
#   válida -> reservada.
# - Si es "y" u "o" aisladas -> operador lógico (con chequeo de límites).
# - En cualquier otro caso -> IDENTIFICADOR (se conserva el texto original).


PATRON_IDENTIFICADOR = re.compile(r"[^\W\d]\w*", re.UNICODE)


def leer_identificador(codigo, posicion):
    
    #Devuelve (tipo, valor, nueva_posicion).
    #tipo puede ser: PALABRA_RESERVADA, IDENTIFICADOR, Y, O.
    
    match = PATRON_IDENTIFICADOR.match(codigo, posicion)
    if not match:
        return None, None, posicion

    texto = match.group()
    fin = match.end()
    minus = texto.lower()

    # Operador lógico de palabra (y / o)
    # "y" y "o" son de una sola letra: islower/isupper ya cubren y/Y, o/O.
    if minus in OPERADORES_PALABRA and forma_valida(texto):
        return OPERADORES_PALABRA[minus], minus, fin

    # Palabra reservada: debe estar en el set Y tener forma válida
    if minus in PALABRAS_RESERVADAS and forma_valida(texto):
        return "PALABRA_RESERVADA", minus, fin

    # Identificador normal (se conserva el texto original)
    return "IDENTIFICADOR", texto, fin


# 9. LECTURA DE CADENAS
# Solo comillas dobles. Error si no cierra en la misma línea o en EOF.


def leer_cadena(codigo, posicion, linea, columna, errores):
    """Devuelve (token, nueva_posicion)."""
    posicion += 1  # saltar comilla de apertura
    inicio = posicion

    while posicion < len(codigo) and codigo[posicion] != '"':
        if codigo[posicion] == "\n":
            # Cadena sin cerrar en la línea
            errores.agregar("Cadena sin cerrar", linea, columna, '"')
            return None, posicion
        posicion += 1

    if posicion >= len(codigo):
        errores.agregar("Cadena sin cerrar (fin de archivo)", linea, columna, '"')
        return None, posicion

    valor = codigo[inicio:posicion]
    posicion += 1  # saltar comilla de cierre

    return crear_token("CADENA", valor, linea, columna), posicion



# 10. LECTURA DE OPERADORES
# CRÍTICO: ordenar por longitud descendente para que "++" gane a "+",
# "==" gane a "=", "<-" gane a "<", etc.

def leer_operador(codigo, posicion):
    """Devuelve (tipo, valor, nueva_posicion) o (None, None, posicion)."""
    # Ordenar por longitud descendente (más largo primero)
    for simbolo in sorted(OPERADORES, key=len, reverse=True):
        if codigo.startswith(simbolo, posicion):
            return OPERADORES[simbolo], simbolo, posicion + len(simbolo)
    return None, None, posicion


# 11. LECTURA DE SÍMBOLOS
# ( ) : ,


def leer_simbolo(codigo, posicion):
    """Devuelve (tipo, valor, nueva_posicion) o (None, None, posicion)."""
    if posicion < len(codigo):
        caracter = codigo[posicion]
        if caracter in SIMBOLOS:
            return SIMBOLOS[caracter], caracter, posicion + 1
    return None, None, posicion


# 12. CONTROL DE INDENTACIÓN
# Cada nivel debe ser múltiplo de 4 espacios. Se emiten INDENT/DEDENT.


def analizar_indentacion(espacios, niveles, tokens, linea, errores):
    """Compara la sangría actual con el nivel anterior y emite INDENT/DEDENT."""
    actual = niveles[-1]

    if espacios > actual:
        if espacios % 4 != 0:
            errores.agregar("Sangría incorrecta (múltiplo de 4)",
                            linea, 1, " " * espacios)
            return
        niveles.append(espacios)
        tokens.append(crear_token("INDENT", espacios, linea, 1))

    elif espacios < actual:
        while espacios < niveles[-1]:
            niveles.pop()
            tokens.append(crear_token("DEDENT", espacios, linea, 1))
        if espacios != niveles[-1]:
            errores.agregar("Sangría inconsistente", linea, 1, " " * espacios)



# 13. ACTUALIZACIÓN DE LÍNEA/COLUMNA
# Tras consumir un fragmento (comentario multilínea, cadena con \n, etc.)


def actualizar_posicion(texto, linea, columna):
    """Actualiza (linea, columna) tras consumir 'texto'."""
    saltos = texto.count("\n")
    if saltos > 0:
        linea += saltos
        columna = len(texto.rsplit("\n", 1)[-1]) + 1
    else:
        columna += len(texto)
    return linea, columna



# 14. FUNCIÓN PRINCIPAL: ANALIZAR
# Recorre el código y devuelve (tokens, administrador_errores).


def analizar(codigo):
    
    #Analiza el código fuente y devuelve (tokens, errores).
    #- tokens: lista de dicts {tipo, valor, linea, columna}
    #- errores: AdministradorErrores con los errores encontrados
    
    tokens = []
    errores = AdministradorErrores()
    niveles = [0]

    posicion = 0
    linea = 1
    columna = 1

    inicio_linea = True      # ¿Estamos al inicio de una línea?
    espacios = 0             # Espacios contados al inicio de línea
    linea_con_codigo = False # ¿La línea actual ya emitió algún token?

    while posicion < len(codigo):
        caracter = codigo[posicion]

        # ---------- SALTO DE LÍNEA ----------
        if caracter == "\n":
            if linea_con_codigo:
                tokens.append(crear_token("NEWLINE", "\n", linea, columna))
            posicion += 1
            linea += 1
            columna = 1
            inicio_linea = True
            espacios = 0
            linea_con_codigo = False
            continue

        # ---------- ESPACIOS ----------
        if caracter == " ":
            if inicio_linea:
                espacios += 1
            posicion += 1
            columna += 1
            continue

        # ---------- TABULACIONES (prohibidas) ----------
        if caracter == "\t":
            errores.agregar("Usa 4 espacios, no tabulaciones", linea, columna, "\t")
            posicion += 1
            columna += 1
            continue

        # ---------- COMENTARIOS d> ... <d ----------
        if codigo.startswith("d>", posicion):
            nueva_pos = leer_comentario(codigo, posicion + 2)
            fragmento = codigo[posicion:nueva_pos]
            linea, columna = actualizar_posicion(fragmento, linea, columna)
            posicion = nueva_pos
            continue

        # ---------- INDENTACIÓN AL INICIO DE LÍNEA ----------
        if inicio_linea:
            analizar_indentacion(espacios, niveles, tokens, linea, errores)
            inicio_linea = False

        # ---------- NÚMEROS ----------
        if caracter.isdigit():
            valor, nueva_pos = leer_numero(codigo, posicion)
            tokens.append(crear_token("NUMERO", valor, linea, columna))
            columna += nueva_pos - posicion
            posicion = nueva_pos
            linea_con_codigo = True
            continue

        # ---------- IDENTIFICADORES / RESERVADAS / y / o ----------
        if PATRON_IDENTIFICADOR.match(codigo, posicion):
            tipo, valor, nueva_pos = leer_identificador(codigo, posicion)
            tokens.append(crear_token(tipo, valor, linea, columna))
            columna += nueva_pos - posicion
            posicion = nueva_pos
            linea_con_codigo = True
            continue

        # ---------- CADENAS ----------
        if caracter == '"':
            token, nueva_pos = leer_cadena(codigo, posicion, linea, columna, errores)
            if token is not None:
                tokens.append(token)
                linea_con_codigo = True
            columna += nueva_pos - posicion
            posicion = nueva_pos
            continue

        # ---------- OPERADORES ----------
        tipo, valor, nueva_pos = leer_operador(codigo, posicion)
        if tipo is not None:
            tokens.append(crear_token(tipo, valor, linea, columna))
            columna += nueva_pos - posicion
            posicion = nueva_pos
            linea_con_codigo = True
            continue

        # ---------- SÍMBOLOS ----------
        tipo, valor, nueva_pos = leer_simbolo(codigo, posicion)
        if tipo is not None:
            tokens.append(crear_token(tipo, valor, linea, columna))
            columna += nueva_pos - posicion
            posicion = nueva_pos
            linea_con_codigo = True
            continue

        # ---------- CARÁCTER NO RECONOCIDO ----------
        errores.agregar("Carácter no reconocido", linea, columna, caracter)
        posicion += 1
        columna += 1

    # ---------- FINALIZAR ÚLTIMA LÍNEA ----------
    if linea_con_codigo:
        tokens.append(crear_token("NEWLINE", "\n", linea, columna))

    # ---------- CERRAR NIVELES DE INDENTACIÓN ----------
    while len(niveles) > 1:
        niveles.pop()
        tokens.append(crear_token("DEDENT", 0, linea, columna))

    # ---------- EOF ----------
    tokens.append(crear_token("EOF", "", linea, columna))

    return tokens, errores
