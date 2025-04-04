import argparse, datetime, random


def main():
    parser = argparse.ArgumentParser(description="Generador de Algogrillas")
    parser.add_argument(
        "-s", "--solucion", action="store_true", help="imprimir la solución"
    )
    parser.add_argument("-n", "--numero", help="número de algogrilla")
    args = parser.parse_args()

    if args.numero and args.numero.isdigit():
        numero_de_algogrilla = int(args.numero)
    else:
        numero_de_algogrilla = int(datetime.datetime.now().timestamp())
    random.seed(numero_de_algogrilla)

    imprimir_solucion = args.solucion  # es True si el usuario incluyó la opción -s

    while True:
        frase, columna, autor = generar_linea_de_frases_random()
        if not frase and not columna and not autor:
            break
        linea_frase_random = (frase, columna, autor)
        subfrases = generar_subfrases(linea_frase_random)
        palabras_info = buscar_palabra(subfrases)
        buscar_otra_algogrilla = verificar_algogrilla(
            palabras_info, numero_de_algogrilla, imprimir_solucion, autor, frase
        )
        if not buscar_otra_algogrilla:
            break
        print(
            "No se encontraron todas las coincidencias necesarias para armar la algogrilla con la frase generada. Se procede a ejecutar otra"
        )


def verificar_algogrilla(
    palabras_info, numero_de_algogrilla, imprimir_solucion, autor, frase
):
    """La funcion se encarga de verificar que la algogrilla generada cumpla los requisitos para ser valida:
    de serlo continua la ejecucion con normalidad, sino devuelve False, lo que provoca que se genere una nueva algogrilla
    """
    (
        palabras_encontradas,
        silabas_de_palabras_encontradas,
        definiciones_de_palabras_encontradas,
        largo_minimo_de_algogrilla,
    ) = palabras_info
    if largo_minimo_de_algogrilla == "Error":  # no encontro el archivo de palabras
        return False
    if len(palabras_encontradas) == largo_minimo_de_algogrilla:
        diccionario_palabras, diccionario_definiciones, diccionario_silabas = (
            crear_diccionarios(
                palabras_encontradas,
                silabas_de_palabras_encontradas,
                definiciones_de_palabras_encontradas,
            )
        )
        mostrar_algogrilla(
            diccionario_palabras,
            diccionario_definiciones,
            diccionario_silabas,
            numero_de_algogrilla,
            imprimir_solucion,
            autor,
            frase,
        )
        return False
    return True


def mostrar_algogrilla(
    diccionario_palabras,
    diccionario_definiciones,
    diccionario_silabas,
    numero_de_algogrilla,
    imprimir_solucion,
    autor,
    frase,
):
    """
    La funcion se encarga de mostar la algogrilla dependiendo de si se ingreso -s durante la ejecucion(imprimir_solucion = True).
    De ser asi, se muestra la algogrilla con las respuestas y termina la ejecucion, por el contrario, si no se ingreso el '-s', se
    continua la ejecucion normal de la algogrilla(respuestas asterisquedas y bucle hasta que el usuario corte la ejecucion o la complete)
    """
    print()
    print(f"ALGOGRILLA NUMERO {numero_de_algogrilla}")
    estado_algogrilla(
        diccionario_palabras,
        diccionario_definiciones,
        diccionario_silabas,
        imprimir_solucion,
        autor,
    )

    if not imprimir_solucion:
        manejar_ingreso_usuario(
            diccionario_palabras,
            diccionario_definiciones,
            diccionario_silabas,
            autor,
            frase,
        )


def manejar_ingreso_usuario(
    diccionario_palabras, diccionario_definiciones, diccionario_silabas, autor, frase
):
    """La funcion se encarga de pedir el numero de palabra al usuario. Si el ingreso es '0',
    se corta la ejecucion del programa y se muestra la frase de la algogrilla, sino se manda el ingreso
    como parametro a otra funcion que decide si la algogrilla fue completada, y de ser asi finaliza la ejecucion
    del programa mostrando un mensaje de felicitaciones"""
    while True:
        ingreso_del_usuario = input("Ingrese un numero de palabra o 0 para terminar: ")
        if ingreso_del_usuario == "0":
            print(f"La frase era: {frase}")
            break
        termino_el_juego = actualizar_pantalla(
            ingreso_del_usuario,
            diccionario_palabras,
            diccionario_definiciones,
            diccionario_silabas,
            autor,
        )
        if termino_el_juego:
            print("¡¡¡¡¡FELICIDADES COMPLETASTE LA ALGOGRILLA!!!!!")
            break


def generar_linea_de_frases_random():
    """La funcion genera un numero de linea random(sabiendo la cantidad de lineas del archivo csv)
    y al encontrarla devuelve sus componentes: frase,columna,autor(todos strings)"""
    try:
        with open("frases.csv", "r", encoding="utf-8", errors="replace") as frases_csv:
            lineas_totales = []
            for linea in frases_csv:
                lineas_totales.append(linea)
            linea_random = random.choice(lineas_totales)
            linea_random = linea_random.rstrip("\n")
            frase, columna, autor = linea_random.split("|")
            try:
                frase = frase.split("(")
                frase = frase[0]
            except (
                ValueError
            ):  # si la frase no tiene "(primera parte)" o "(conclusion)"
                pass
            return frase, columna, autor
    except FileNotFoundError:
        print("No se encontro el archivo de frases")
        return None, None, None


def generar_subfrases(linea_frase):
    """La funcion recibe la linea del archivo frases.csv elegida al azar por parametro, normaliza la frase y la devuelve dividida a la mitad (2 strings)
    ;en el caso de ser impar,la primera parte siempre es mayor a la segunda. Ademas devuelve las columnas:str(para seguir el flujo de datos)
    """
    frase_normalizada, columnas, _ = normalizar_frase(linea_frase)
    mitad = (len(frase_normalizada) + 1) // 2
    subfrase_1 = frase_normalizada[:mitad]
    subfrase_2 = frase_normalizada[mitad:]
    return subfrase_1, subfrase_2, columnas


def normalizar_frase(linea_frase):
    """La funcion recibe la linea completa de la frase generada al azar, normaliza la frase(la convierte toda a minusculas y le saca las tildes)
    , y devuelve la frase normalizada, las columnas y su autor (todos strings)"""
    try:
        frase, cols, autor = linea_frase
    except TypeError:
        raise TypeError(
            "ERROR FATAL, El archivo de frases esta vacio, o la informacion contenida no corresponde a la esperada"
        )

    vocales = "aeiou"
    vocales_con_tilde = "áéíóú"
    frase_normalizada = ""
    frase_en_minusculas = frase.lower()
    for caracter in frase_en_minusculas:
        if caracter.isalpha():
            if caracter in vocales_con_tilde:
                for indice in range(len(vocales_con_tilde)):
                    if caracter == vocales_con_tilde[indice]:
                        frase_normalizada += vocales[indice]
            else:
                frase_normalizada += caracter
    return frase_normalizada, cols, autor


def normalizar_letra(letra):
    """Recibe una letra, la convierte en minuscula y la devuelve, a no ser que sea una vocal con tilde,
    que la convierte en la vocal sin tilde y la devuelve(en minuscula)"""
    vocales_con_tilde = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ü": "u"}
    letra_minuscula = letra.lower()
    if letra_minuscula in vocales_con_tilde:
        return vocales_con_tilde[letra_minuscula]
    return letra_minuscula


def formato_palabra(palabra, col_1, col_2):
    """La funcion recibe una palabra y 2 columnas. Forma la palabra_formateada dependiendo de si la columna_2 esta vacia o no.
    Devuelve asi la palabra recibida por parametro en minuscula menos las letras que se encuentran en las columnas recibidas por parametro
    """
    if col_2 != "":
        palabra_formateada = (
            palabra[:col_1].lower()
            + palabra[col_1].upper()
            + palabra[col_1 + 1 : col_2].lower()
            + palabra[col_2].upper()
            + palabra[col_2 + 1 :]
        )
    else:
        palabra_formateada = (
            palabra[:col_1].lower()
            + palabra[col_1].upper()
            + palabra[col_1 + 1 :].lower()
        )
    return palabra_formateada


def buscar_palabra(subfrases_y_cols):
    """La funcion recibe por parametro una lista con las subfrases generadas y las columnas, luego recorre cada caracter de las subfrases a la vez,
    buscando en palabras.csv coincidencias de esas letras en las posiciones indicadas por las columnas; al hallar coincidencias deja de buscar esas letras y pasa a las proximas.
    Si la subfrase_1 tiene mas caracteres que subfrase_2, busca una palabra que tenga menos cantidad de caracteres que el numero de columna_2,
    y que coincida en la posicion que indica la columna_1 la ultima letra de subfrase_1.
    Ademas, las comparaciones las realiza de manera tal que si las letras tienen tildes las ignora pero luego las guarda.
    Devuelve asi, una lista con todas las coincidencias encontradas(las cuales tienen las letras en las columnas indicadas en mayusculas),
    otra con todas las definciones, otra con las silabas de cada palabra encontrada,y el largo de la subfrase_1 para verificar
    que la cantidad de palabras encontradas sea igual al largo de la subfrase_1 (una palabra encontrada por letra de subfrase_1)
    """
    subfrase_1, subfrase_2, columnas = subfrases_y_cols
    columna_1, columna_2 = columnas.split(",")
    columna_1, columna_2 = int(columna_1) - 1, int(columna_2) - 1
    palabras_encontradas = []
    lineas_totales = []
    silabas_totales = []
    definiciones_totales = []
    try:
        with open(
            "palabras.csv", "r", encoding="utf-8", errors="replace"
        ) as palabras_csv:
            for linea in palabras_csv:
                lineas_totales.append(linea)
    except FileNotFoundError:
        print("No se encontro el archivo de palabras")
        return "", "", "", "Error"
    for indice in range(len(subfrase_1)):
        palabras_posibles = {}
        for line in lineas_totales:
            line = line.rstrip("\n")
            palabra, silabas, definicion = line.split("|")
            letra_1 = subfrase_1[indice]
            if indice != len(subfrase_2):
                letra_2 = subfrase_2[indice]
            else:
                letra_2 = ""
            if (
                len(palabra) >= columna_2 + 1
                and normalizar_letra(palabra[columna_1]) == letra_1
                and letra_2 != ""
                and normalizar_letra(palabra[columna_2]) == letra_2
            ):
                palabra = formato_palabra(palabra, columna_1, columna_2)
                palabras_posibles[palabra] = (silabas, definicion)
            elif (
                letra_2 == ""
                and len(palabra) >= columna_1 + 1
                and normalizar_letra(palabra[columna_1]) == letra_1
                and len(palabra) < columna_2 + 1
            ):
                palabra = formato_palabra(palabra, columna_1, "")
                palabras_posibles[palabra] = (silabas, definicion)

        claves = palabras_posibles.keys()
        if claves:
            palabra_random = random.choice(list(claves))
            palabras_encontradas.append(palabra_random)
            silabas_totales.append(palabras_posibles[palabra_random][0])
            definiciones_totales.append(palabras_posibles[palabra_random][1])
        else:
            return "", "", "", 1

    return palabras_encontradas, silabas_totales, definiciones_totales, len(subfrase_1)


def crear_diccionarios(
    palabras: list[str], silabas_totales: list[str], definiciones: list[str]
):
    """La funcion recibe las listas con todas las palabras generadas por la funcion buscar_palabra() , y devuelve 3 diccionarios, uno para cada
    parametro recibidos"""
    diccionario_silabas = {}
    diccionario_definiciones = {}
    diccionario_palabras = {}
    for indicador in range(len(palabras)):
        diccionario_silabas[palabras[indicador]] = silabas_totales[indicador]
        diccionario_definiciones[indicador + 1] = definiciones[indicador]
        diccionario_palabras[palabras[indicador]] = "*" * len(palabras[indicador])
    return diccionario_palabras, diccionario_definiciones, diccionario_silabas


def estado_algogrilla(
    diccionario_palabras: dict,
    diccionario_definiciones: dict,
    diccionario_silabas: dict,
    mostrar_solucion: bool,
    autor: str,
):
    """La funcion recibe los diccionarios que contienen todas las palabras, definiciones y silabas, y si fueron encontradas por el usuario,
    y se encarga de generar la tablilla con la que interactuara el usuario.
    Devuelve True o False, dependiendo de si todas las palabras fueron encontradas por el usuario o no.
    """

    print()
    indicar_columnas_con_astericos = ""
    for palabra in diccionario_palabras.keys():
        for caracter in palabra:
            if caracter.isupper():
                indicar_columnas_con_astericos += "*"
            else:
                indicar_columnas_con_astericos += " "
        print("   " + indicar_columnas_con_astericos)
        break

    contador = 0
    for palabra in diccionario_palabras:
        contador += 1
        if mostrar_solucion:
            if contador < 10:
                print(contador, "", palabra)
            else:
                print(contador, palabra)
        else:
            if contador < 10:
                print(contador, "", diccionario_palabras[palabra])
            else:
                print(contador, diccionario_palabras[palabra])
    print()
    print("DEFINICIONES")
    for numero, definicion in diccionario_definiciones.items():
        if definicion != "":
            print(numero, definicion)
    print()

    lista_silabas = []
    for silabas in diccionario_silabas.values():
        silabas_separadas = silabas.split("-")
        for silaba in silabas_separadas:
            lista_silabas.append(silaba)
    lista_silabas.sort()
    print(",".join(lista_silabas))
    print()
    print(f"Al finalizar leerá una frase de {autor}.")
    print()

    if len(diccionario_silabas) == 0:
        return True
    return False


def validar_ingreso_numero_de_palabra(ingreso_de_usuario, diccionario_definiciones):
    """Valida el numero de palabra ingresado por el usuario y devuelve la definición seleccionada
    o None en caso de no hallarla(o haber un error de ingreso)"""
    if not ingreso_de_usuario.isdigit():
        print("El ingreso debe ser un número entero")
        print()
        return None

    indice = int(ingreso_de_usuario)
    if indice in diccionario_definiciones:
        definicion_seleccionada = diccionario_definiciones[indice]
        if definicion_seleccionada == "":
            print("El número de palabra ingresado ya se encuentra resuelto")
            print()
            return None
        return definicion_seleccionada
    else:
        print("El ingreso debe ser un número de palabra que esté en la algogrilla")
        print()
        return None


def validar_ingreso_palabra(definicion_seleccionada):
    """Valida que la palabra ingresada por el usuario contenga caracteres alphabeticos,
    y devuelve la palabra normalizada; sino devuelve None"""
    palabra_ingresada_normalizada = ""
    pedir_palabra = input(f"{definicion_seleccionada} :")

    if len(pedir_palabra) == 0:
        print("Inválido, ingreso vacío")
        print()
        return None

    for letra in pedir_palabra:
        if letra.isalpha():
            palabra_ingresada_normalizada += normalizar_letra(letra)
        else:
            print(
                "El ingreso de la palabra debe contener letras (no caracteres especiales ni números)"
            )
            print()
            return None
    return palabra_ingresada_normalizada


def actualizar_pantalla(
    ingreso_de_usuario,
    diccionario_palabras,
    diccionario_definiciones,
    diccionario_silabas,
    autor,
):
    """La funcion actualiza los diccionarios y el estado del juego según si el ingreso de usuario coincide
    con las palabras en la grilla, y devuelve si el juego terminó(booleano)"""
    definicion_seleccionada = validar_ingreso_numero_de_palabra(
        ingreso_de_usuario, diccionario_definiciones
    )
    if definicion_seleccionada is None:
        return
    palabra_ingresada_normalizada = validar_ingreso_palabra(definicion_seleccionada)
    if palabra_ingresada_normalizada is None:
        return
    coincidencia = False
    for palabra in diccionario_palabras:
        palabra_diccionario_normalizada = "".join(
            normalizar_letra(letra) for letra in palabra
        )

        if palabra_diccionario_normalizada == palabra_ingresada_normalizada:
            diccionario_palabras[palabra] = palabra
            coincidencia = True
            break

    if coincidencia:
        print("¡Correcto!")
        print()
        del diccionario_silabas[palabra]
        contador = list(diccionario_palabras.keys()).index(palabra) + 1
        diccionario_definiciones[contador] = ""
    else:
        print(
            f"La palabra {palabra_ingresada_normalizada} no es la respuesta. ¡Siga intentando!"
        )
        print()
        return

    fin_del_juego = estado_algogrilla(
        diccionario_palabras,
        diccionario_definiciones,
        diccionario_silabas,
        False,
        autor,
    )
    return fin_del_juego


main()
