# Lexer para cadenas y caracteres

# Funcion para reconocer cadenas con comillas dobles
def leer_cadena(codigo, i):
    cant = len(codigo)    # Guarda el total de caracteres
    texto = ""     # Variabe vacia que va guardando el contenido de la cadena
    i = i + 1      # Avanza 1 posicion que salta la comilla de apertura

    # Recorre letra por letra mientras aun hayan caracteres
    while i < cant and codigo[i] != '"' and codigo[i] != "\n":
        texto = texto + codigo[i]      # Agrega el caracter leido
        i = i + 1      # Pasa a la siguiente posicion

    # Comprueba que tenga la comilla de cierre
    if i < cant and codigo[i] == '"':
        print("CADENA:", texto)
        i = i + 1
    else:
        print("ERROR: Cadena sin cerrar")
    return i      # Devuelve posicion actualizada

# Funcion para reconocer caracteres con comillas simples
def leer_caracter(codigo, i):
    cant = len(codigo)
    texto = ""
    i = i + 1

    # Recorre letra por letra mientras aun hayan caracteres
    while i < cant and codigo[i] != "'" and codigo[i] != "\n":
        texto = texto + codigo[i]
        i = i + 1

    # Comprueba que se haya cerrado la comilla simple
    if i < cant and codigo[i] == "'":
        # Verifica que el caracter solo tenga longitud de 1
        if len(texto) == 1:
            print("CARACTER:", texto)
        else:
            print("ERROR: Caracter invalido")
        i = i + 1
    else:
        print("ERROR: Caracter sin cerrar")
    return i


# Funcion principal que recorre el codigo
def analizar(codigo):
    i = 0
    cant = len(codigo)

    # Recorre el texto hasta el final
    while i < cant:
        # Si hay comilla doble ejecuta la funcion leer_cadea
        if codigo[i] == '"':
            i = leer_cadena(codigo, i)
        # Si hay comilla simple ejecuta la funcion leer_caracter
        elif codigo[i] == "'":
            i = leer_caracter(codigo, i)
        # Si lee otra palabra, espacio o simbolo solo avanza al siguiente caracter
        else:
            i = i + 1


# Codigo de prueba
codigo = '''
huevo nombre <- "Dino Code"
rugir "Hola dino"
huevo edad <- '5'
huevo palabra <- 'Hola'
huevo letra <- 'a'
huevo vacio <- ''
rugir "Prueba
'''
analizar(codigo)