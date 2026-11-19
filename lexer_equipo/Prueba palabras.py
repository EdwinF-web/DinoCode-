"""
Dino Code - Prueba de palabras reservadas
"""

import re

from palabras_reservadas import (
    PALABRAS_RESERVADAS,
    SIMBOLO_COMENTARIO,
    TipoToken,
    clasificar,
)

class AnalizadorPalabras:
    """Recorre un programa Dino code y clasifica cada palabra que encuentra."""

    # Palabra = letra o _ seguida de letras, dígitos o _  (acepta tildes y ñ)
    PATRON_PALABRA = re.compile(r"[^\W\d]\w*")
    PATRON_CADENA = re.compile(r'"[^"\n]*"')
    # "d>" solo cuenta como comentario si NO va pegado a otra letra.
    # Así "edad>=10" no se confunde con un comentario.
    PATRON_COMENTARIO = re.compile(r"(?<!\w)" + re.escape(SIMBOLO_COMENTARIO))

    def analizar(self, codigo: str):
        """Devuelve una lista de (linea, palabra, TipoToken)."""
        resultado = []
        for numero_linea, texto in enumerate(codigo.splitlines(), start=1):
            texto = self._quitar_comentario(texto)
            texto = self.PATRON_CADENA.sub(" ", texto)  # lo que va entre comillas no cuenta
            for palabra in self.PATRON_PALABRA.findall(texto):
                resultado.append((numero_linea, palabra, clasificar(palabra)))
        return resultado

    def _quitar_comentario(self, texto: str) -> str:
        m = self.PATRON_COMENTARIO.search(texto)
        return texto[: m.start()] if m else texto

    def reservadas_usadas(self, codigo: str):
        """Conjunto con los tipos de palabras reservadas que aparecen."""
        return {
            tipo
            for _, _, tipo in self.analizar(codigo)
            if tipo != TipoToken.IDENTIFICADOR
        }


# ----------------------------------------------------------------------
# 2. Pruebas con assert (si algo falla, avisame cuál chewin)--
def probar_cada_reservada():
    for texto, tipo_esperado in PALABRAS_RESERVADAS.items():
        assert clasificar(texto) == tipo_esperado, f"Falló con '{texto}'"
    print(f"OK  {len(PALABRAS_RESERVADAS)} palabras reservadas clasificadas bien")


def probar_mayusculas():
    for variante in ["Si_ve", "SI_VE", "si_ve", "sI_Ve"]:
        assert clasificar(variante) == TipoToken.SI_VE, f"Falló con '{variante}'"
    print("OK  No importa si se escribe en mayúsculas o minúsculas")


def probar_identificadores():
    for nombre in ["nombre", "edad", "cali", "pi", "i", "n", "huevos", "rugido"]:
        assert clasificar(nombre) == TipoToken.IDENTIFICADOR, f"Falló con '{nombre}'"
    print("OK  Los nombres normales son IDENTIFICADOR (incluso 'huevos' y 'rugido')")


def probar_programa():
    programa = """\
huevo nombre <- "Dino code"
huevo edad <- captura "Dame tu dino edad"
huevo cali <- captura "Dame tu promedio"
huevo pi = 3.141516   d> constante, no cuenta si_ve ni huevo

Si_ve edad>=10 haz
    rugir "eres dino pro"
no_ve
    rugir "no eres dino pro"
    si_ve cali = 10.0 haz
        rugir "eres pro"
    o_ve cali >= 9.0 y cali < 9.9 haz
        rugir "Échale ganas"
    fin_si
fin_si
"""
    analizador = AnalizadorPalabras()
    palabras = analizador.analizar(programa)

    print("\n--- Palabras encontradas en el programa ---")
    for linea, palabra, tipo in palabras:
        print(f"línea {linea:>2}  {palabra:<8} -> {tipo.name}")

    tipos = [tipo for _, _, tipo in palabras]
    # Los textos entre comillas y el comentario no deben contarse
    assert tipos.count(TipoToken.HUEVO) == 4, "Debe haber 4 'huevo'"
    assert tipos.count(TipoToken.RUGIR) == 4, "Debe haber 4 'rugir'"
    assert tipos.count(TipoToken.SI_VE) == 2, "El 'si_ve' del comentario no cuenta"
    assert tipos.count(TipoToken.FIN_SI) == 2
    assert TipoToken.O_VE in tipos and TipoToken.NO_VE in tipos and TipoToken.Y in tipos
    assert "edad" in [p for _, p, t in palabras if t == TipoToken.IDENTIFICADOR]

    print("\nOK  El programa de ejemplo se analizó bien")


if __name__ == "__main__":
    probar_cada_reservada()
    probar_mayusculas()
    probar_identificadores()
    probar_programa()