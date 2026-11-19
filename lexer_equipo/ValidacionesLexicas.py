import re

# 1. VALIDAR NUMEROS ENTEROS Y DECIMALES

def numero_valido(numero):

    patron = r"^[0-9]+(\.[0-9]+)?$"

    return re.fullmatch(patron, numero) is not None


# 2. VALIDAR CADENAS DE TEXTO

def cadena_cerrada(cadena):

    if len(cadena) < 2:
        return False

    comilla = cadena[0]

    if comilla not in ('"', "'"):
        return False

    return cadena[-1] == comilla


# 3. VALIDAR CARACTERES PERMITIDOS

def caracter_valido(caracter):

    simbolos = "+-*/=<>()[]{}.,:;\"'#_"

    if caracter.isalnum():
        return True

    if caracter.isspace():
        return True

    if caracter in simbolos:
        return True

    return False


# 4. VALIDAR IDENTIFICADORES

def identificador_valido(nombre):

    patron = r"^[a-zA-Z_][a-zA-Z0-9_]*$"

    return re.fullmatch(patron, nombre) is not None


# 5. VALIDAR UN ELEMENTO SEGUN SU TIPO

def validar_elemento(elemento, tipo):

    if tipo == "numero":
        return numero_valido(elemento)

    elif tipo == "cadena":
        return cadena_cerrada(elemento)

    elif tipo == "identificador":
        return identificador_valido(elemento)

    elif tipo == "caracter":
        return caracter_valido(elemento)

    return False


# PRUEBAS INDEPENDIENTES

if __name__ == "__main__":

    print("===== VALIDACIONES DINOCODE =====")

    print("\nNUMEROS:")

    for numero in ["15", "9.5", "12.5.6", "15.", ".25"]:

        print(numero, numero_valido(numero))

    print("\nCADENAS:")

    for cadena in ['"Hola"', '"DinoCode', "'Hola'"]:

        print(cadena, cadena_cerrada(cadena))

    print("\nIDENTIFICADORES:")

    for nombre in ["edad", "nombre1", "_dato", "123edad"]:

        print(nombre, identificador_valido(nombre))

    print("\nCARACTERES:")

    for caracter in ["@", "$", "+", "A"]:

        print(caracter, caracter_valido(caracter))
