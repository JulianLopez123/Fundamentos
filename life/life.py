"""
Conway's Game of Life
---------------------

https://es.wikipedia.org/wiki/Juego_de_la_vida

El "tablero de juego" es una malla formada por cuadrados ("células") que se
extiende por el infinito en todas las direcciones. Cada célula tiene 8 células
vecinas, que son las que están próximas a ella, incluidas las diagonales. Las
células tienen dos estados: están "vivas" o "muertas" (o "encendidas" y
"apagadas"). El estado de la malla evoluciona a lo largo de unidades de tiempo
discretas (se podría decir que por turnos). El estado de todas las células se
tiene en cuenta para calcular el estado de las mismas al turno siguiente.
Todas las células se actualizan simultáneamente.

Las transiciones dependen del número de células vecinas vivas:

* Una célula muerta con exactamente 3 células vecinas vivas "nace" (al turno
  siguiente estará viva).
* Una célula viva con 2 ó 3 células vecinas vivas sigue viva, en otro caso
  muere o permanece muerta (por "soledad" o "superpoblación").
"""


def main():
    """
    Función principal del programa. Crea el estado inicial de Game of Life
    y muestra la simulación paso a paso mientras que el usuario presione
    Enter.
    """
    life = life_crear(
        [
            "..........",
            "..........",
            "..........",
            ".....#....",
            "......#...",
            "....###...",
            "..........",
            "..........",
        ]
    )
    while True:
        for linea in life_mostrar(life):
            print(linea)
        print()
        input("Presione Enter para continuar, CTRL+C para terminar")
        print()
        life = life_siguiente(life)


# -----------------------------------------------------------------------------


def life_crear(mapa: list[str]) -> list[list]:
    """
    Crea el estado inicial de Game of life a partir de una disposición
    representada con los caracteres '.' y '#'.

    `mapa` debe ser una lista de cadenas, donde cada cadena representa una
    fila del tablero, y cada caracter puede ser '.' (vacío) o '#' (célula).
    Todas las filas deben tener la misma cantidad de caracteres.

    Devuelve el estado del juego, que es una lista de listas donde cada
    sublista representa una fila, y cada elemento de la fila es False (vacío)
    o True (célula).
    """
    estado_del_juego = []
    for filas in range(len(mapa)):
        lista = []
        for columna in mapa[filas]:
            if columna == ".":
                lista.append(False)
            else:
                lista.append(True)
        estado_del_juego.append(lista)

    return estado_del_juego


# -----------------------------------------------------------------------------


def life_mostrar(life: list[list]) -> list[str]:
    """
    Crea una representación del estado del juego para mostrar en pantalla.

    Recibe el estado del juego (inicialmente creado con life_crear()) y
    devuelve una lista de cadenas con la representación del tablero para
    mostrar en la pantalla. Cada una de las cadenas representa una fila
    y cada caracter debe ser '.' (vacío) o '#' (célula).
    """
    lista = []
    for fila in range(len(life)):
        string = ""
        for columna in range(len(life[fila])):
            if life[fila][columna]:
                string += "#"
            else:
                string += "."
        lista.append(string)
    return lista


# -----------------------------------------------------------------------------


def cant_adyacentes(life, f, c):
    """
    Calcula la cantidad de células adyacentes a la celda en la fila `f` y la
    columna `c`.

    Importante: El "tablero" se considera "infinito": las celdas del borde
    izquierdo están conectadas a la izquierda con las celdas del borde
    derecho, y viceversa. Las celdas del borde superior están conectadas hacia
    arriba con las celdas del borde inferior, y viceversa.
    """
    celulas_adyacentes = 0
    for fila in range(f - 1, f + 2):
        for columna in range(c - 1, c + 2):
            if len(life) != 1:
                if fila == len(life):
                    fila = 0
            else:
                if fila == len(life):
                    fila = -fila

            if columna == len(life[fila]):
                columna = -columna

            if life[fila][columna] and (fila, columna) != (f, c):
                celulas_adyacentes += 1

    return celulas_adyacentes


# -----------------------------------------------------------------------------


def celda_siguiente(life, f, c):
    """
    Calcula el estado siguiente de la celda ubicada en la fila `f` y la
    columna `c`.

    Devuelve True si en la celda (f, c) habrá una célula en la siguiente
    iteración, o False si la celda quedará vacía.
    """
    celda = life[f][c]
    n = cant_adyacentes(life, f, c)
    if n == 3:
        return True
    if celda:
        if n == 2:
            return True
    return False


# -----------------------------------------------------------------------------


def life_siguiente(life):
    """
    Calcula el siguiente estado del juego.

    Recibe el estado actual del juego (lista de listas de False/True) y
    devuelve un _nuevo_ estado que representa la siguiente iteración según las
    reglas del juego.

    Importante: El "tablero" se considera "infinito": las celdas del borde
    izquierdo están conectadas a la izquierda con las celdas del borde
    derecho, y viceversa. Las celdas del borde superior están conectadas hacia
    arriba con las celdas del borde inferior, y viceversa.
    """
    siguiente = []
    for f in range(len(life)):
        fila = []
        for c in range(len(life[0])):
            fila.append(celda_siguiente(life, f, c))
        siguiente.append(fila)
    return siguiente


# -----------------------------------------------------------------------------

# Esta parte del código se ejecuta al final, asegurando que se ejecute el programa
# mediante la terminal correctamente y permitiendo que se puedan realizar
# los tests de forma automática y aislada.
if __name__ == "__main__":
    main()
