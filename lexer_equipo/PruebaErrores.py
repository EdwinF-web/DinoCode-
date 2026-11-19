
from ErroresLexicos import AdministradorErrores
from ValidacionesLexicas import (
    numero_valido,
    cadena_cerrada,
    caracter_valido
)


# ANALIZAR EL CODIGO FUENTE

def analizar_codigo(codigo):

    errores = AdministradorErrores()

    lineas = codigo.splitlines()

    for numero_linea, texto in enumerate(lineas, start=1):

        columna = 1
        dentro_cadena = False
        comilla_inicio = None
        posicion_inicio = None

        while columna <= len(texto):

            caracter = texto[columna - 1]

            # DETECTAR CADENAS
            if caracter in ('"', "'"):

                if not dentro_cadena:

                    dentro_cadena = True
                    comilla_inicio = caracter
                    posicion_inicio = columna

                elif caracter == comilla_inicio:

                    dentro_cadena = False
                    comilla_inicio = None
                    posicion_inicio = None

                columna += 1
                continue

            # IGNORAR CONTENIDO DE CADENAS
            if dentro_cadena:

                columna += 1
                continue

            # DETECTAR NUMEROS
            if caracter.isdigit():

                inicio = columna

                while columna <= len(texto):

                    actual = texto[columna - 1]

                    if actual.isdigit() or actual == ".":
                        columna += 1
                    else:
                        break

                numero = texto[inicio - 1:columna - 1]

                if not numero_valido(numero):

                    errores.error_numero_mal_formado(
                        numero,
                        numero_linea,
                        inicio
                    )

                continue

            # PERMITIR LETRAS, ESPACIOS Y GUIONES BAJOS
            if caracter.isalpha() or caracter == "_" or caracter.isspace():

                columna += 1
                continue

            # VALIDAR OTROS CARACTERES
            if caracter_valido(caracter):

                columna += 1
                continue

            # REGISTRAR CARACTER DESCONOCIDO
            errores.error_caracter_desconocido(
                caracter,
                numero_linea,
                columna
            )

            columna += 1

        # COMPROBAR CADENA SIN CERRAR
        if dentro_cadena:

            if not cadena_cerrada(comilla_inicio):

                errores.error_cadena_sin_cerrar(
                    comilla_inicio,
                    numero_linea,
                    posicion_inicio
                )

    return errores


# PROGRAMA PRINCIPAL

def main():

    print("       BIENVENIDO A DINOCODE")

    print("\nEscribe tu codigo DinoCode.")
    print("Escribe FIN para terminar.")
    print("------------------------------------")

    codigo = []

    # RECIBIR CODIGO DEL USUARIO

    while True:

        try:
            linea = input("DinoCode >> ")

        except EOFError:
            break

        if linea.strip() == "FIN":
            break

        codigo.append(linea)

    # UNIR LAS LINEAS
    codigo_fuente = "\n".join(codigo)

    # ANALIZAR CODIGO
    errores = analizar_codigo(codigo_fuente)

    # MOSTRAR RESULTADOS

    print("          RESULTADO DINOCODE")

    if errores.tiene_errores():

        errores.mostrar_errores()

        print("\nTotal de errores:", errores.cantidad_errores())

    else:

        print("No se encontraron errores lexicos.")
        print("El codigo paso la revision lexica.")

    print("\nFin del analisis.")


# EJECUTAR PROGRAMA

if __name__ == "__main__":

    main()
