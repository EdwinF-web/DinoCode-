from Numeros import *
# Esta parte solo corre si ejecutas Numeros.py directamente
if __name__ == "__main__":
    entrada = input("Ingrese numeros enteros, decimales y valores boleanos: ")
    resultado = analizar_numeros(entrada)
    if resultado is not None:
        for tipo, val in resultado:
            print(tipo, val)