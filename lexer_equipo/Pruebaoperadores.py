from operadores import reconocer_operador

codigo = """
huevo edad <- 15

si_ve edad >= 10 y edad <= 20 haz
    rugir "edad correcta"
fin_si

si_ve edad < 5 o edad > 30 haz
    rugir "fuera del rango de edad"
fin_si
d<fin del codigo>d
"""

posicion = 0

while posicion < len(codigo):

    resultado = reconocer_operador(codigo, posicion)

    if resultado is not None:

        print(
            "Tipo:", resultado["tipo"],
            "| Valor:", resultado["valor"]
        )

        posicion += resultado["longitud"]

    else:
        posicion += 1