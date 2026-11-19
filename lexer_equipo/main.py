from lexerCerregido7 import analizar


codigo = """
huevo nombre <- "DinoCode"
huevo edad <- 18
huevo pi = 3.141516

si_ve edad >= 10 haz
    rugir "Eres dinosaurio"
no_ve
    rugir "No eres dinosaurio"
fin_si

cazar desde i hasta 5 avanzar
    rugir "Estamos cazando"
fin_caza

d> Este es un comentario

d> Este es un comentario
de varias lineas <d
"""

try:

    tokens = analizar(codigo)

    print("TOKENS GENERADOS POR DinoCode")
    print("--------------------------------")

    for token in tokens:
        print(token)

except SyntaxError as error:
    print("Error léxico:", error)