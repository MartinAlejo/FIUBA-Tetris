import tetris
import gamelib
import math

ESPERA_DESCENDER = 8

TAMANIO_BLOQUE = 30 # El bloque es un cuadrado, y el tamaño es en pixeles

MARGEN_LATERAL_JUEGO = 100 # Es el margen que se deja respecto del lateral izquierdo de la pantalla para dibujar el juego

MARGEN_LATERAL_MARCO = 550 # Es el margen que se deja respecto del lateral izquierdo de la pantalla para dibujar la puntuacion y la siguiente pieza

ANCHO_PANTALLA = 800

ALTO_PANTALLA = 600

LONGITUD_MARCO = 100 # Es la longitud de cada lado del cuadrado que enmarca a la siguiente pieza y la puntuacion

GAME_OVER_X, GAME_OVER_Y = 600, 200 # Son las coordenadas 'x' e 'y' en la que se mostrara el cartel de "GAME OVER" cuando el juego esta finalizado

RUTA_GUARDADO = "save.txt"

def dibujar_grilla():
    """
    Dibuja la grilla en la pantalla
    """
    altura = 0
    ancho = 0
    ancho_final = tetris.ANCHO_JUEGO * TAMANIO_BLOQUE
    altura_final = tetris.ALTO_JUEGO * TAMANIO_BLOQUE
    y = TAMANIO_BLOQUE
    x = MARGEN_LATERAL_JUEGO

    # El siguiente bloque, dibuja las lineas horizontales
    while altura <= altura_final:
        # En este while "x" es cte, en el siguiente while muta
        gamelib.draw_line(x, y, ancho_final + x, y)
        y += TAMANIO_BLOQUE
        altura += TAMANIO_BLOQUE

    # El siguiente bloque, dibuja las lineas verticales
    while ancho <= ancho_final:
        gamelib.draw_line(x, TAMANIO_BLOQUE, x, altura)
        x += TAMANIO_BLOQUE
        ancho += TAMANIO_BLOQUE


def dibujar_puntuacion(puntuacion = 0):
    """
    Dibuja y muestra la puntuacion en la pantalla
    """
    # La puntuacion aumenta en 1 por cada vez que se consolida una pieza (se calcula en el main)
    dist = LONGITUD_MARCO
    x_inic = MARGEN_LATERAL_MARCO
    x_fin = x_inic + dist
    y_inic = 300
    y_fin = y_inic + dist
    tamaño_num = 24

    # Dibuja las lineas horizontales
    gamelib.draw_line(x_inic, y_inic + 15, x_fin, y_inic + 15)
    gamelib.draw_line(x_inic, y_fin, x_fin, y_fin)

    # Dibuja las lineas verticales
    gamelib.draw_line(x_inic, y_inic + 15, x_inic, y_fin)
    gamelib.draw_line(x_fin, y_inic + 15, x_fin, y_fin)

    # Dibuja la puntuacion
    gamelib.draw_text("Puntuacion:", x_inic + dist // 2, y_inic, size = 12)
    gamelib.draw_text(puntuacion, x_inic + dist // 2, y_inic + (dist + tamaño_num) // 2, size = tamaño_num)


def dibujar_siguiente_pieza(siguiente_pieza):
    """
    Muestra la siguiente pieza en la pantalla
    """
    # Primero dibujamos un marco y un texto para legibilidad, dentro del marco dibujamos la pieza
    dist = LONGITUD_MARCO
    x_inic = MARGEN_LATERAL_MARCO 
    x_fin = x_inic + dist
    y_inic = 40
    y_fin = y_inic + dist
    gamelib.draw_text("Siguiente pieza:", x_inic + dist // 2, y_inic, size = 12)

    # Dibuja las lineas horizontales
    gamelib.draw_line(x_inic, y_inic + 15, x_fin, y_inic + 15)
    gamelib.draw_line(x_inic, y_fin, x_fin, y_fin)

    # Dibuja las lineas verticales
    gamelib.draw_line(x_inic, y_inic + 15, x_inic, y_fin)
    gamelib.draw_line(x_fin, y_inic + 15, x_fin, y_fin)

    # Dibuja la siguiente pieza
    for pos in siguiente_pieza:
        x = pos[0] * TAMANIO_BLOQUE // 2
        y = pos[1] * TAMANIO_BLOQUE // 2
        x1 = x_inic + x + dist // 3
        y1 = y_inic + y + dist // 3
        x2 = x_inic + TAMANIO_BLOQUE // 2 + x + dist // 3
        y2 = y_inic + TAMANIO_BLOQUE // 2 + y + dist // 3
        gamelib.draw_rectangle(x1, y1, x2, y2)


def mostrar_juego(juego, siguiente_pieza, puntuacion):
    """
    Actualiza el estado de juego en la pantalla
    """
    # Primero dibujamos la grilla
    dibujar_grilla()
    dibujar_siguiente_pieza(siguiente_pieza)
    dibujar_puntuacion(puntuacion)

    x_1 = MARGEN_LATERAL_JUEGO
    x_2 = x_1 + TAMANIO_BLOQUE
    y_1 = TAMANIO_BLOQUE
    y_2 = y_1 + TAMANIO_BLOQUE
    
    # Ahora recorremos la grilla, y dibujamos el estado de juego
    for fila in juego:
        for col in fila:  
            if col == tetris.CAR_PIEZA:
                gamelib.draw_rectangle(x_1, y_1, x_2, y_2, outline='white', fill='blue')

            if col == tetris.CAR_SUPERFICIE:
                gamelib.draw_rectangle(x_1, y_1, x_2, y_2, outline='white', fill='green')

            if col == tetris.CAR_TERMINADO:
                # Marcamos de color rojo la/s posicion/es de la pieza actual, que colisiono/colisionaron con la superficie consolidada
                gamelib.draw_rectangle(x_1, y_1, x_2, y_2, outline='white', fill='red')
                gamelib.draw_text("GAME OVER", GAME_OVER_X, GAME_OVER_Y, size = 24, fill = 'red')

            x_1 += TAMANIO_BLOQUE
            x_2 += TAMANIO_BLOQUE

        x_1 = MARGEN_LATERAL_JUEGO
        x_2 = x_1 + TAMANIO_BLOQUE
        y_1 += TAMANIO_BLOQUE
        y_2 += TAMANIO_BLOQUE


def guardar_puntuacion(nombre, puntuacion):
    import csv
    cont_lineas = 0
    punt_min = math.inf
    linea_punt_min = 0
    nombre_puntuaciones = []
    agregar = False
    cambiar = False

    # Recorremos el archivo para obtener la "cantidad de lineas", la "menor puntuacion" y la "linea de la menor puntuacion"
    with open("puntajes.txt", "r") as archivo:
        lector = csv.reader(archivo, delimiter = ":")
        for linea in lector:
            nombre_puntuaciones.append(linea)
            _, punt_ant = linea
            if int(punt_ant) < punt_min:
                punt_min = int(punt_ant)
                linea_punt_min = cont_lineas
            cont_lineas += 1

    # Verificamos que hacer, si no hacer nada o si debe cambiar/agregar la puntuacion
    if cont_lineas < 10:
        agregar = True
    elif punt_min < puntuacion:
        cambiar = True
    elif punt_min >= puntuacion:
        return

    # Modificamos el archivo en funcion de si se debe agregar o cambiar la puntuacion
    if agregar:
        with open("puntajes.txt", "a") as archivo:
            archivo.write(f"{nombre}:{puntuacion}\n")
    elif cambiar:
        with open("puntajes.txt", "w") as archivo:
            nombre_puntuaciones[linea_punt_min] = [nombre, puntuacion]
            for linea in nombre_puntuaciones:
                jugador, puntos = linea
                archivo.write(f"{jugador}:{puntos}\n")


def mostrar_puntuaciones():
    from operator import itemgetter
    import csv
    x_inic = ANCHO_PANTALLA / 2
    y_inic = TAMANIO_BLOQUE
    l_puntuaciones = []

    # Obtenemos la lista de puntuaciones
    gamelib.draw_text("Puntuaciones:", x_inic, y_inic, size = 24)
    with open("puntajes.txt") as archivo:
        lector = csv.reader(archivo, delimiter = ":")
        for jug, punt in lector:
            punt = int(punt)
            l_puntuaciones.append([jug, punt])

    # Ordenamos las puntuaciones y las mostramos en pantalla
    l_puntuaciones.sort(key = itemgetter(1), reverse = True)
    for nombre, puntuacion in l_puntuaciones:
        y_inic += 50
        gamelib.draw_text(f"{nombre}: {puntuacion}", x_inic, y_inic, size = 12)

            
def main():
    # Inicializar el estado del juego
    pieza_inic = tetris.generar_pieza()
    siguiente_pieza = tetris.generar_pieza()
    juego = tetris.crear_juego(pieza_inic)
    gamelib.resize(ANCHO_PANTALLA, ALTO_PANTALLA)
    timer_bajar = ESPERA_DESCENDER
    salir = False
    puntuacion = 0

    while gamelib.loop(fps=30):
        gamelib.draw_begin()
        mostrar_juego(juego, siguiente_pieza, puntuacion)
        gamelib.draw_end()

        # En el caso de que el juego se terminó, se pide el nombre al usuario para guardar su puntuacion
        if tetris.terminado(juego):
            nombre = gamelib.input("Ingrese su nombre")
            while not nombre:
                nombre = gamelib.input("Ingrese su nombre")
            try:
                guardar_puntuacion(nombre, puntuacion)
                break
            except FileNotFoundError:
                break

        for event in gamelib.get_events():
            if not event:
                break
            if event.type == gamelib.EventType.KeyPress:
                tecla = event.key
                # Actualizar el juego, según la tecla presionada
                if tecla == 'Escape':
                    exit()

                if tecla == 'Right' or tecla == 'd':
                    if not tetris.terminado(juego):
                        juego = tetris.mover(juego, tetris.DERECHA)

                if tecla == 'Left' or tecla == 'a':
                    if not tetris.terminado(juego):
                        juego = tetris.mover(juego, tetris.IZQUIERDA)

                if tecla == 'Down' or tecla == 's':
                    if not tetris.terminado(juego):
                        # Desciendo la pieza y sumo la puntuacion
                        juego, siguiente_pieza = tetris.descender_pieza(juego, siguiente_pieza)
                        puntuacion += 1

                if tecla == 'w' or tecla == 'r':
                    if not tetris.terminado(juego):
                        juego = tetris.rotar(juego)

                if tecla == 'g':
                    if not tetris.terminado(juego):
                        tetris.guardar_partida(juego, puntuacion, siguiente_pieza, RUTA_GUARDADO)

                if tecla == 'c':
                    if not tetris.terminado(juego):
                        try:
                            juego, puntuacion, siguiente_pieza = tetris.cargar_partida(RUTA_GUARDADO)
                        except FileNotFoundError:
                            print("No hay archivo de guardado")
        timer_bajar -= 1
        if timer_bajar == 0:
            timer_bajar = ESPERA_DESCENDER
            # Descender la pieza automáticamente
            juego, cambiar_pieza = tetris.avanzar(juego, siguiente_pieza)
            if cambiar_pieza:
                siguiente_pieza = tetris.generar_pieza()
                puntuacion += 1

    # Ahora mostramos la tabla de puntuaciones
    while gamelib.loop(fps=30):
        gamelib.draw_begin()
        try:
            mostrar_puntuaciones()
        except FileNotFoundError:
            f = open("puntajes.txt", "w")
            f.close()
            guardar_puntuacion(nombre, puntuacion)
            mostrar_puntuaciones()
        gamelib.draw_end()

        for event in gamelib.get_events():
            if not event:
                break
            if event.type == gamelib.EventType.KeyPress:
                tecla = event.key
                if tecla == 'Escape':
                    exit()

gamelib.init(main)