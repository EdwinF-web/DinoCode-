# PRUEBA DEL LEXER DINOCODE 
# Analiza el código objetivo del equipo y muestra:
#   - Todos los tokens generados (tipo, valor, línea, columna)
#   - Todos los errores léxicos encontrados

from lexer import analizar



# CÓDIGO OBJETIVO (el que debe aceptar DinoCode)

CODIGO = '''huevo nombre <-"dino"
Huevo edad <- captura ("dame tu edad")
huevo cali <- Captura("dame tu calificacion en decimal ")
huevo pi = 3.1416 d> estos es un cometario para decir que asi debe de declar 
una constante en el codigo no es nesesario cerrar el comentario en una sola lienas <d
si_ve edad >= 10 haz:
    rugir("Eres dinoMayor de edad")
no_ve 
    rugir "No eres dinomayor de edad "
    si_ve cali = 10.0 haz:
        rugir "eres dinopro"
    o_ve cali >=9.0 y cali <=9.9 haz:
        rugir "Vas bien dino"
    fin_si
Fin_Si d>FIN_SI 

Huevo i <-0
huevo dame <- CAPTURAR("DAME un numero")
cazar desde i hasta n avanzar i++:
    RUGIR ("preza conseguida "# i) d> # es para concatenar
Fin_caza
    '''


def main():
    print("=" * 60)
    print("ANÁLISIS LÉXICO DINOCODE")
    print("=" * 60)

    tokens, errores = analizar(CODIGO)

    # ---------- TOKENS ----------
    print("\n--- TOKENS GENERADOS ---")
    print(f"{'#':<4} {'TIPO':<20} {'VALOR':<20} {'LÍNEA':<6} {'COL':<5}")
    print("-" * 60)

    for i, t in enumerate(tokens, start=1):
        valor = repr(t["valor"]) if t["valor"] != "\n" else "\\n"
        print(f"{i:<4} {t['tipo']:<20} {valor:<20} {t['linea']:<6} {t['columna']:<5}")

    # ---------- ERRORES ----------
    print("\n--- ERRORES LÉXICOS ---")
    if errores.tiene_errores():
        errores.mostrar()
        print(f"\nTotal de errores: {errores.cantidad()}")
    else:
        print("No se encontraron errores léxicos.")
        print("El código pasó la revisión léxica. ✅")

    # ---------- RESUMEN ----------
    print("\n--- RESUMEN ---")
    print(f"Total de tokens: {len(tokens)}")
    print(f"Total de errores: {errores.cantidad()}")

    # ---------- VERIFICACIONES CLAVE ----------
    print("\n--- VERIFICACIONES CLAVE ---")

    tipos = [t["tipo"] for t in tokens]

    checks = [
        ("Se reconoce 'huevo' (minúsculas)",
         "huevo" in [t["valor"] for t in tokens if t["tipo"] == "PALABRA_RESERVADA"]),
        ("Se reconoce 'Huevo' (Primera_mayúscula) como reservada",
         any(t["tipo"] == "PALABRA_RESERVADA" and t["valor"] == "huevo" for t in tokens)),
        ("Se reconoce 'Captura' (Primera_mayúscula) como captura",
         "captura" in [t["valor"] for t in tokens if t["tipo"] == "PALABRA_RESERVADA"]),
        ("Se reconoce 'CAPTURAR' como captura",
         any(t["tipo"] == "PALABRA_RESERVADA" and t["valor"] == "captura" for t in tokens)),
        ("Se reconoce 'si_ve'",
         "si_ve" in [t["valor"] for t in tokens if t["tipo"] == "PALABRA_RESERVADA"]),
        ("Se reconoce 'Fin_Si' como fin_si",
         "fin_si" in [t["valor"] for t in tokens if t["tipo"] == "PALABRA_RESERVADA"]),
        ("Se reconoce 'cazar' (ciclo)",
         "cazar" in [t["valor"] for t in tokens if t["tipo"] == "PALABRA_RESERVADA"]),
        ("Se reconoce 'fin_caza'",
         "fin_caza" in [t["valor"] for t in tokens if t["tipo"] == "PALABRA_RESERVADA"]),
        ("Se reconoce ':' (DOS_PUNTOS)",
         "DOS_PUNTOS" in tipos),
        ("Se reconoce '#' (CONCATENA)",
         "CONCATENA" in tipos),
        ("Se reconoce '++' (INCREMENTO)",
         "INCREMENTO" in tipos),
        ("Se reconoce 'y' como operador Y",
         "Y" in tipos),
        ("Se reconoce '>=' (MAYOR_IGUAL)",
         "MAYOR_IGUAL" in tipos),
        ("Se reconoce '<-' (ASIGNA)",
         "ASIGNA" in tipos),
        ("Se reconoce '=' (ASIGNA_CONSTANTE)",
         "ASIGNA_CONSTANTE" in tipos),
        ("Se reconoce '3.1416' como NUMERO",
         "NUMERO" in tipos and "3.1416" in [t["valor"] for t in tokens]),
        ("Se reconoce cadena \"dino\"",
         "CADENA" in tipos and "dino" in [t["valor"] for t in tokens]),
        ("Se emite EOF al final",
         tipos[-1] == "EOF"),
        ("Se emite INDENT tras 'haz:'",
         "INDENT" in tipos),
        ("Se emite DEDENT al cerrar bloques",
         "DEDENT" in tipos),
        ("El comentario 'd> ...' se ignora (no hay token de comentario)",
         not any("COMENTARIO" in t["tipo"] for t in tokens)),
    ]

    for descripcion, ok in checks:
        marca = "✅" if ok else "❌"
        print(f"{marca} {descripcion}")

    


if __name__ == "__main__":
    main()
