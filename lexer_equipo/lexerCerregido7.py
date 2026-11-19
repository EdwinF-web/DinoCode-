# DINOCODE - ANALIZADOR LEXICO

PALABRAS_RESERVADAS = {
     "huevo", "captura", "rugir", "si_ve", "no_ve", "o_ve",
     "haz", "fin_si", "cazar", "desde", "hasta", "avanzar",
     "fin_caza"
}

OPERADORES = {
      "<-", ">=", "<=", "=", "!=",
      "+", "-", "*", "/", "==", "<",
      ">"
}


# ==========================================
# 1. AQUI ES PARA CREAR UN TOKEN


def crear_token(tipo, valor, linea, columna):
    return {
        "tipo": tipo,
        "valor": valor,
        "linea": linea,
        "columna": columna
    }


# ==========================================
# 2. AQUI ES PARA LEER NUMEROS


def leer_numero(codigo, posicion, linea, columna):
    inicio = posicion

    while posicion < len(codigo) and codigo[posicion].isdigit():
        posicion += 1

    if (posicion < len(codigo)
            and codigo[posicion] == "."
            and posicion + 1 < len(codigo)
            and codigo[posicion + 1].isdigit()):

        posicion += 1

        while posicion < len(codigo) and codigo[posicion].isdigit():
            posicion += 1

    valor = codigo[inicio:posicion]

    token = crear_token("NUMERO", valor, linea, columna)

    return token, posicion


# ==========================================
# 3. AQUI ES PARA LEER LOS IDENTIFICADORES


def leer_identificador(codigo, posicion, linea, columna):
    inicio = posicion

    while posicion < len(codigo):
        caracter = codigo[posicion]

        if caracter.isalnum() or caracter == "_":
            posicion += 1
        else:
            break

    valor = codigo[inicio:posicion]

    if valor in PALABRAS_RESERVADAS:
        tipo = "PALABRA_RESERVADA"
    else:
        tipo = "IDENTIFICADOR"

    token = crear_token(tipo, valor, linea, columna)

    return token, posicion


# ==========================================
# 4. AQUI ES PARA LEER LAS PALABRAS CON GUION


def leer_palabra_con_guion(codigo, posicion, linea, columna):
    palabras = sorted(PALABRAS_RESERVADAS, key=len, reverse=True)

    for palabra in palabras:

        if codigo.startswith(palabra, posicion):

            fin = posicion + len(palabra)

            if (fin == len(codigo)
                    or not (codigo[fin].isalnum()
                            or codigo[fin] in "_-")):

                token = crear_token(
                    "PALABRA_RESERVADA",
                    palabra,
                    linea,
                    columna
                )

                return token, fin

    return None, posicion


# ==========================================
# 5. AQUI ES PARA LEER LAS CADENAS DE TEXTO


def leer_cadena(codigo, posicion, linea, columna):
    posicion += 1
    inicio = posicion

    while posicion < len(codigo) and codigo[posicion] != '"':

        if codigo[posicion] == "\n":
            raise SyntaxError(
                f"Cadena sin cerrar en linea {linea}, columna {columna}"
            )

        posicion += 1

    if posicion >= len(codigo):
        raise SyntaxError(
            f"Cadena sin cerrar en linea {linea}, columna {columna}"
        )

    valor = codigo[inicio:posicion]
    posicion += 1

    token = crear_token("CADENA", valor, linea, columna)

    return token, posicion


# ==========================================
# 6. AQUI ES PARA LEER LOS OPERADORES


def leer_operador(codigo, posicion, linea, columna):

    for operador in OPERADORES:

        if codigo.startswith(operador, posicion):

            token = crear_token(
                "OPERADOR",
                operador,
                linea,
                columna
            )

            return token, posicion + len(operador)

    return None, posicion


# ==========================================
# 7. AQUI ES PARA LEER SIMBOLOS


def leer_simbolo(codigo, posicion, linea, columna):

    simbolos = {
        "(": "PARENTESIS_IZQ",
        ")": "PARENTESIS_DER",
        ",": "COMA"
    }

    caracter = codigo[posicion]

    if caracter in simbolos:

        token = crear_token(
            simbolos[caracter],
            caracter,
            linea,
            columna
        )

        return token, posicion + 1

    return None, posicion


# ==========================================
# 8. AQUI ES PARA LEER LOS COMENTARIOS


def leer_comentario(codigo, posicion):

    inicio_contenido = posicion + 2

    # Buscar el cierre de comentario multilinea
    cierre = codigo.find("<d", inicio_contenido)

    if cierre != -1:
        return cierre + 2

    # Si no hay cierre, es comentario de una linea
    salto = codigo.find("\n", inicio_contenido)

    if salto != -1:
        return salto

    return len(codigo)


# ==========================================
# 9. AQUI ES PARA ACTUALIZAR LINEAS Y COLUMNAS


def actualizar_posicion(codigo, inicio, fin, linea, columna):

    texto = codigo[inicio:fin]
    saltos = texto.count("\n")

    if saltos > 0:
        linea += saltos
        columna = len(texto.rsplit("\n", 1)[-1]) + 1
    else:
        columna += len(texto)

    return linea, columna


# ==========================================
# 10. AQUI ES PARA ANALIZAR LA SANGRIA


def analizar_indentacion(espacios, niveles, tokens, linea):

    actual = niveles[-1]

    if espacios > actual:

        if espacios % 4 != 0:
            raise SyntaxError(
                f"Sangria incorrecta en linea {linea}"
            )

        niveles.append(espacios)

        tokens.append(
            crear_token("INDENT", espacios, linea, 1)
        )

    elif espacios < actual:

        while espacios < niveles[-1]:

            niveles.pop()

            tokens.append(
                crear_token("DEDENT", espacios, linea, 1)
            )

        if espacios != niveles[-1]:
            raise SyntaxError(
                f"Sangria inconsistente en linea {linea}"
            )


# ==========================================
# 11. AQUI ES PARA ANALIZAR TODO EL CODIGO


def analizar(codigo):

    tokens = []
    niveles = [0]

    posicion = 0
    linea = 1
    columna = 1

    inicio_linea = True
    espacios = 0
    linea_con_codigo = False

    while posicion < len(codigo):

        caracter = codigo[posicion]

        # SALTOS DE LINEA
        if caracter == "\n":

            if linea_con_codigo:
                tokens.append(
                    crear_token("NEWLINE", "\n", linea, columna)
                )

            posicion += 1
            linea += 1
            columna = 1

            inicio_linea = True
            espacios = 0
            linea_con_codigo = False

            continue

        # ESPACIOS
        if caracter == " ":

            if inicio_linea:
                espacios += 1

            posicion += 1
            columna += 1

            continue

        # TABULACIONES
        if caracter == "\t":
            raise SyntaxError(
                f"Usa cuatro espacios, no tabulaciones, en linea {linea}"
            )

        # COMENTARIOS
        if codigo.startswith("d>", posicion):

            nueva_posicion = leer_comentario(codigo, posicion)

            linea, columna = actualizar_posicion(
                codigo, posicion, nueva_posicion, linea, columna
            )

            posicion = nueva_posicion

            continue

        # SANGRIA AL INICIO DE LINEA
        if inicio_linea:

            analizar_indentacion(
                espacios, niveles, tokens, linea
            )

            inicio_linea = False

        # PALABRAS CON GUION
        if caracter.isalpha():

            token, nueva_posicion = leer_palabra_con_guion(
                codigo, posicion, linea, columna
            )

            if token is not None:

                tokens.append(token)
                columna += nueva_posicion - posicion
                posicion = nueva_posicion
                linea_con_codigo = True

                continue

        # NUMEROS
        if caracter.isdigit():

            token, nueva_posicion = leer_numero(
                codigo, posicion, linea, columna
            )

            tokens.append(token)
            columna += nueva_posicion - posicion
            posicion = nueva_posicion
            linea_con_codigo = True

            continue

        # IDENTIFICADORES
        if caracter.isalpha() or caracter == "_":

            token, nueva_posicion = leer_identificador(
                codigo, posicion, linea, columna
            )

            tokens.append(token)
            columna += nueva_posicion - posicion
            posicion = nueva_posicion
            linea_con_codigo = True

            continue

        # CADENAS
        if caracter == '"':

            token, nueva_posicion = leer_cadena(
                codigo, posicion, linea, columna
            )

            tokens.append(token)
            columna += nueva_posicion - posicion
            posicion = nueva_posicion
            linea_con_codigo = True

            continue

        # OPERADORES
        token, nueva_posicion = leer_operador(
            codigo, posicion, linea, columna
        )

        if token is not None:

            tokens.append(token)
            columna += nueva_posicion - posicion
            posicion = nueva_posicion
            linea_con_codigo = True

            continue

        # SIMBOLOS
        token, nueva_posicion = leer_simbolo(
            codigo, posicion, linea, columna
        )

        if token is not None:

            tokens.append(token)
            columna += nueva_posicion - posicion
            posicion = nueva_posicion
            linea_con_codigo = True

            continue

        # CARACTER NO RECONOCIDO
        raise SyntaxError(
            f"Caracter no reconocido '{caracter}' "
            f"en linea {linea}, columna {columna}"
        )

    # FINALIZAR LA ULTIMA LINEA
    if linea_con_codigo:
        tokens.append(
            crear_token("NEWLINE", "\n", linea, columna)
        )

    # CERRAR NIVELES DE SANGRIA
    while len(niveles) > 1:

        niveles.pop()

        tokens.append(
            crear_token("DEDENT", 0, linea, columna)
        )

    return tokens