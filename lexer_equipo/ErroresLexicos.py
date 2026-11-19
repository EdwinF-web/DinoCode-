# CLASE 1: REPRESENTAR UN ERROR LEXICO

class ErrorLexico:

    def __init__(self, mensaje, linea, columna, caracter):

        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna
        self.caracter = caracter

    # Generar mensaje del error
    def mostrar_error(self):

        return (
            f"Error lexico: {self.mensaje} "
            f"'{self.caracter}' "
            f"en linea {self.linea}, columna {self.columna}"
        )


# CLASE 2: ADMINISTRAR LOS ERRORES

class AdministradorErrores:

    def __init__(self):

        self.errores = []


    # REGISTRAR UN ERROR GENERAL
    def agregar_error(self, mensaje, linea, columna, caracter):

        error = ErrorLexico(
            mensaje,
            linea,
            columna,
            caracter
        )

        self.errores.append(error)

        return error


    # ERROR 1: CARACTER NO RECONOCIDO
    def error_caracter_desconocido(self, caracter, linea, columna):

        return self.agregar_error(
            "Caracter no reconocido",
            linea,
            columna,
            caracter
        )


    # ERROR 2: NUMERO MAL FORMADO
    def error_numero_mal_formado(self, numero, linea, columna):

        return self.agregar_error(
            "Numero mal formado",
            linea,
            columna,
            numero
        )


    # ERROR 3: CADENA SIN CERRAR
    def error_cadena_sin_cerrar(self, cadena, linea, columna):

        return self.agregar_error(
            "Cadena de texto sin cerrar",
            linea,
            columna,
            cadena
        )


    # ERROR 4: CARACTER NO PERMITIDO
    def error_caracter_no_permitido(self, caracter, linea, columna):

        return self.agregar_error(
            "Caracter no permitido",
            linea,
            columna,
            caracter
        )


    # ERROR 5: OTRO ERROR LEXICO
    def error_personalizado(self, mensaje, elemento, linea, columna):

        return self.agregar_error(
            mensaje,
            linea,
            columna,
            elemento
        )


    # MOSTRAR TODOS LOS ERRORES
    def mostrar_errores(self):

        if not self.errores:
            print("No se encontraron errores lexicos.")
            return

        print("\n========== ERRORES DINOCODE ==========")

        for numero, error in enumerate(self.errores, start=1):

            print(f"\nError numero {numero}")
            print(error.mostrar_error())

        print("\n======================================")


    # CONTAR ERRORES
    def cantidad_errores(self):

        return len(self.errores)


    # COMPROBAR SI EXISTEN ERRORES
    def tiene_errores(self):

        return len(self.errores) > 0


    # LIMPIAR LISTA DE ERRORES
    def limpiar_errores(self):

        self.errores.clear()
