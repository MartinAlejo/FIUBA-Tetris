from random import *
import csv

ANCHO_JUEGO, ALTO_JUEGO = 9, 18
IZQUIERDA, DERECHA = -1, 1
CUBO = 0
Z = 1
S = 2
I = 3
L = 4
L_INV = 5
T = 6

def obtener_piezas():
    """
    Abre el archivo 'piezas.txt', lo recorre y me devuelve una tupla de tuplas de tuplas con el siguiente formato piezas[la_pieza][0:4]

    Desde la posicion 0 a 4 (sin incluir), tenemos la posicion original de la pieza, luego en el caso de que hayan rotaciones posibles,
    seran [4:8]...[n*4:n*4 + 4]

    El 'CUBO' tiene solo posicion original... la 'Z','S','I' tienen solo una rotacion posible. El resto de piezas tienen 3 rotaciones posibles (ademas de sus posiciones originales)

    Si por ejemplo quiero la 'primer' rotacion de la pieza 'L': piezas[L][4:8]
    """

    piezas = []
    with open("piezas.txt") as archivo:
        lector = csv.reader(archivo, delimiter = " ")
        for linea in lector:
            linea = linea[:-2]
            la_pieza = []

            for pieza in linea:
                posiciones = pieza.split(";")
                for posicion in posiciones:
                    posicion = posicion.split(",")
                    # Convertimos cada elemento de posicion a entero
                    for ind, elem in enumerate(posicion):
                        posicion[ind] = int(elem)
                    la_pieza.append(tuple(posicion))

            piezas.append(tuple(la_pieza))


    return tuple(piezas)

PIEZAS = obtener_piezas()
#Declaro las siguientes constantes, para que quede claro que representa cada caracter, y por ende conseguir un codigo 
#mas mantenible

CAR_PIEZA = "x"
CAR_VACIO = ""
CAR_SUPERFICIE = "o"
CAR_TERMINADO = "f"

def generar_pieza(pieza=None):
    """
    Genera una nueva pieza de entre PIEZAS al azar. Si se especifica el parámetro pieza
    se generará una pieza del tipo indicado. Los tipos de pieza posibles
    están dados por las constantes CUBO, Z, S, I, L, L_INV, T.

    El valor retornado es una tupla donde cada elemento es una posición
    ocupada por la pieza, ubicada en (0, 0). Por ejemplo, para la pieza
    I se devolverá: ( (0, 0), (0, 1), (0, 2), (0, 3) ), indicando que 
    ocupa las posiciones (x = 0, y = 0), (x = 0, y = 1), ..., etc.
    """
    if pieza is None:
        pieza = randint(0, 6)

    if pieza == CUBO:
        return PIEZAS[pieza][0:4]
    if pieza == Z:
        return PIEZAS[pieza][0:4]
    if pieza == S:
        return PIEZAS[pieza][0:4]
    if pieza == I:
        return PIEZAS[pieza][0:4]
    if pieza == L:
        return PIEZAS[pieza][0:4]
    if pieza == L_INV:
        return PIEZAS[pieza][0:4]
    if pieza == T:
        return PIEZAS[pieza][0:4]


def trasladar_pieza(pieza, dx, dy):
    """
    Traslada la pieza de su posición actual a (posicion + (dx, dy)).

    La pieza está representada como una tupla de posiciones ocupadas,
    donde cada posición ocupada es una tupla (x, y). 
    Por ejemplo para la pieza ( (0, 0), (0, 1), (0, 2), (0, 3) ) y
    el desplazamiento dx=2, dy=3 se devolverá la pieza 
    ( (2, 3), (2, 4), (2, 5), (2, 6) ).
    """    
    pieza_retorno = []
    final = []
    for i in range(len(pieza)):
        pieza_retorno.append(list(pieza[i]))

    for x in pieza_retorno:
        resultado = []
        resultado.append(x[0] + dx)
        resultado.append(x[1] + dy)
        final.append(tuple(resultado))
        

    return tuple(final)


def crear_grilla():
    """
    Crea una grilla vacio, donde el "vacio" se representa con ''
    """
    grilla_tetris_vacia = []
    for i in range(ALTO_JUEGO):
       fila_grilla = []
       for j in range(ANCHO_JUEGO):
           fila_grilla.append(CAR_VACIO)
       grilla_tetris_vacia.append(fila_grilla)

    return grilla_tetris_vacia


def crear_juego(pieza_inicial):
    """
    Crea un nuevo juego de Tetris.

    El parámetro pieza_inicial es una pieza obtenida mediante 
    pieza.generar_pieza. Ver documentación de esa función para más información.

    El juego creado debe cumplir con lo siguiente:
    - La grilla está vacía: hay_superficie da False para todas las ubicaciones
    - La pieza actual está arriba de todo, en el centro de la pantalla.
    - El juego no está terminado: terminado(juego) da False

    Que la pieza actual esté arriba de todo significa que la coordenada Y de 
    sus posiciones superiores es 0 (cero).
    """
    grilla = crear_grilla()
    pieza_centrada = trasladar_pieza(pieza_inicial, ANCHO_JUEGO // 2, 0)

    for i in pieza_centrada:
        x = i[0] 
        y = i[1]
        grilla[y][x] = CAR_PIEZA

    return grilla


def dimensiones(juego):
    """
    Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
    """
    ancho = len(juego[0])
    alto = len(juego)
    return (ancho, alto)


def pieza_actual(juego):
    """
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por la pieza actual.

    Se entiende por pieza actual a la pieza que está cayendo y todavía no
    fue consolidada con la superficie.

    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    #fila = y
    #columna = x
    pieza_actual = []

    for fila in range(len(juego)):
        for columna in range(len(juego[fila])):
            if CAR_PIEZA in juego[fila][columna]:
                pieza_actual.append((columna, fila))


    return tuple(pieza_actual)


def hay_superficie(juego, x, y):
    """
    Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.
    
    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    return juego[y][x] == CAR_SUPERFICIE
    

def mover(juego, direccion):
    """
    Mueve la pieza actual hacia la derecha o izquierda, si es posible.
    Devuelve un nuevo estado de juego con la pieza movida o el mismo estado 
    recibido si el movimiento no se puede realizar.

    El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
    """
    pieza = pieza_actual(juego)
    nueva_pieza = []
    mov_valido = True

    for coordenada in pieza:
        nueva_cor_x = coordenada[0] + direccion
        cor_y = coordenada[1]
        if not 0 <= nueva_cor_x <= ANCHO_JUEGO - 1:
            mov_valido = False
            break

        if juego[cor_y][nueva_cor_x] == CAR_SUPERFICIE:
            mov_valido = False
            break
            
        nueva_pieza.append((nueva_cor_x, coordenada[1]))

    if mov_valido:
        for coordenada in pieza:
            x = coordenada[0]
            y = coordenada[1]
            juego[y][x] = CAR_VACIO

        for coordenada in nueva_pieza:
            x = coordenada[0]
            y = coordenada[1]
            juego[y][x] = CAR_PIEZA

    return juego


def avanzar(juego, siguiente_pieza):
    """
    Avanza al siguiente estado de juego a partir del estado actual.
    
    Devuelve una tupla (juego_nuevo, cambiar_pieza) donde el primer valor
    es el nuevo estado del juego y el segundo valor es un booleano que indica
    si se debe cambiar la siguiente_pieza (es decir, se consolidó la pieza
    actual con la superficie).
    
    Avanzar el estado del juego significa:
     - Descender una posición la pieza actual.
     - Si al descender la pieza no colisiona con la superficie, simplemente
       devolver el nuevo juego con la pieza en la nueva ubicación.
     - En caso contrario, se debe
       - Consolidar la pieza actual con la superficie.
       - Eliminar las líneas que se hayan completado.
       - Cambiar la pieza actual por siguiente_pieza.

    Si se debe agregar una nueva pieza, se utilizará la pieza indicada en
    el parámetro siguiente_pieza. El valor del parámetro es una pieza obtenida 
    llamando a generar_pieza().

    **NOTA:** Hay una simplificación respecto del Tetris real a tener en
    consideración en esta función: la próxima pieza a agregar debe entrar 
    completamente en la grilla para poder seguir jugando, si al intentar 
    incorporar la nueva pieza arriba de todo en el medio de la grilla se
    pisara la superficie, se considerará que el juego está terminado.

    Si el juego está terminado (no se pueden agregar más piezas), la funcion no hace nada, 
    se debe devolver el mismo juego que se recibió.
    """
    old_pieza_actual = pieza_actual(juego)
    cambiar_pieza = False
    consolidar = None
    avanzar = None

    #Verifica si el juego termino, con lo cual devuelve el mismo juego
    if terminado(juego):
        return (juego, cambiar_pieza)

    #El siguiente bloque elimina la pieza del juego, para luego 'avanzarla' e introducirla nuevamente
    for cor in old_pieza_actual:
        x = cor[0]
        y = cor[1]
        juego[y][x] = CAR_VACIO

    #El siguiente bloque recorre la pieza del juego, y verifica si tiene que consolidarla o bajarla
    for cor in old_pieza_actual:
        x = cor[0]
        y = cor[1]

        if (y == ALTO_JUEGO - 1) or hay_superficie(juego, x, y + 1):
            consolidar = True
            cambiar_pieza = True
            avanzar = False
            break        
        else:    
            avanzar = True

    #El siguiente bloque consolida o baja la pieza, segun corresponda
    if consolidar:
        for cor in old_pieza_actual:
            x = cor[0]
            y = cor[1]
            juego[y][x] = CAR_SUPERFICIE

    elif avanzar:
        for cor in old_pieza_actual:
            x = cor[0]
            y = cor[1]
            juego[y + 1][x] = CAR_PIEZA


    #Lo que sigue solo sucede si hay que cambiar la pieza, con lo cual la pieza se consolido y tengo que borrar las filas completas, 
    #como asi tambien meter mi nueva pieza en el juego actualizado.

    if cambiar_pieza:
        for fila in juego:
            if CAR_VACIO in fila:
                continue
            else:
                fila_de_vacios = []
                for longitud in range(len(fila)):
                    fila_de_vacios.append(CAR_VACIO)
                juego.remove(fila)
                juego.insert(0, fila_de_vacios)

        #El siguiente bloque antes de meter la pieza verifica si el juego terminó, en cuyo caso, mete el valor CAR_TERMINADO en la 
        #grilla con el cual la funcion 'terminado' verifica que el juego se perdió. En caso contrario, simplemente se inserta la nueva pieza 

        pieza_centrada = trasladar_pieza(siguiente_pieza, ANCHO_JUEGO // 2, 0)
        for cor in pieza_centrada:
            x = cor[0] 
            y = cor[1]
            if juego[y][x] == CAR_SUPERFICIE:
                juego[y][x] = CAR_TERMINADO
                cambiar_pieza = True #Mis dudas respecto a esta linea, aca el juego termino y no se que booleano deberia devolver (Ya que si bien se intento poner la pieza, tecnicamente no se llego a cambiar en su totalidad). Lo pongo en True porque en la doc. dice que si se consolido, debe devolver True... Y si llego aca, es porque lo hizo (Si efectivamente debe ser True, podria quitar esta linea directamente, pero la dejo de momento por esa ambiguedad)
                #Podria poner/quitar un break, lo que cambia es que con break solo pone un 'CAR_TERMINADO', si lo pongo pone uno por cada situacion de "finish" (que se superpone la pieza con superficie)
                #Otra forma de resolver este problema, es agregarle, y aca (fuera del for, dentro del if) pasarle por parametro a 'terminado' la siguiente pieza
            else:
                juego[y][x] = CAR_PIEZA


    return (juego, cambiar_pieza)


def terminado(juego):
    """
    Devuelve True si el juego terminó, es decir no se pueden agregar
    nuevas piezas, o False si se puede seguir jugando.
    """
    #Un juego que paso por la funcion "avanzar", y llego a un estado de juego en el cual se encuentra "terminado", tendra el carácter_terminado en el mismo
    for linea in juego:
        if CAR_TERMINADO in linea:
            return True

    return False


def descender_pieza(juego, siguiente_pieza):
    bajo = False
    while not bajo:
        pieza_act = pieza_actual(juego)
        for cor in pieza_act:
            x = cor[0]
            y = cor[1]
            if y == ALTO_JUEGO - 1 or hay_superficie(juego, x, y + 1):
                bajo = True

        juego, cambiar_pieza = avanzar(juego, siguiente_pieza)
        if cambiar_pieza:
            siguiente_pieza = generar_pieza()

    return juego, siguiente_pieza


def buscar_rotacion(pieza_en_origen):
    """
    Dada una pieza en el origen (No se refiere a la pieza original, sino con sus coordenadas en el "origen"), devuelve la proxima rotacion

    La 'rotacion_0' es la pieza original
    """
    pieza_rotada = ""
    for pieza in PIEZAS:
        rot_0 = pieza[0:4]
        rot_1 = pieza[4:8]
        rot_2 = pieza[8:12]
        rot_3 = pieza[12:16]
        
        if pieza_en_origen == rot_0:
            pieza_rotada = rot_1

        if pieza_en_origen == rot_1:
            pieza_rotada = rot_2

        if pieza_en_origen == rot_2:
            pieza_rotada = rot_3

        if pieza_en_origen == rot_3:
            pieza_rotada = rot_0

        if pieza_rotada == ():
            return rot_0

        elif len(pieza_rotada) == 4:
            return pieza_rotada


def rotar_pieza(juego):
    """
    Devuelve la posicion de la pieza rotada en el juego
    """
    pieza_ordenada = sorted(pieza_actual(juego))
    x, y = pieza_ordenada[0][0], pieza_ordenada[0][1]
    pieza_en_origen = trasladar_pieza(pieza_ordenada, -x, -y)
    siguiente_rotacion = buscar_rotacion(pieza_en_origen)
    
    return trasladar_pieza(siguiente_rotacion, x, y)


def rotar(juego):
    """
    Rota la pieza en el juego
    """
    pieza_rotada = rotar_pieza(juego)
    old_pieza_actual = pieza_actual(juego)

    #Primero verificamos que al rotar no se salga de la grilla, ni que toque a una superficie consolidada
    for new_pos in pieza_rotada:
        new_x = new_pos[0]
        new_y = new_pos[1]

        if not 0 <= new_x <= ANCHO_JUEGO - 1:
            return juego

        if not 0 <= new_y <= ALTO_JUEGO - 1:
            return juego

        if hay_superficie(juego, new_x, new_y):
            return juego

    #Ahora rotamos la pieza actual en el juego
    for old_pos in old_pieza_actual:
        x = old_pos[0]
        y = old_pos[1]
        juego[y][x] = CAR_VACIO

    for new_pos in pieza_rotada:
        x = new_pos[0]
        y = new_pos[1]
        juego[y][x] = CAR_PIEZA

    return juego


def guardar_partida(juego, puntuacion, siguiente_pieza, ruta):
    """
    Guarda la partida
    """
    juego_aux = ""
    sig_pieza = ""

    # Guardo el juego de una forma que sea mas facil de leer despues cuando lo quiera cargar
    for fila in juego:
        for car in fila:
            if car == CAR_VACIO:
                juego_aux += " "
            juego_aux += car

    # Guardo la siguiente pieza de una forma que sea mas facil de leer cuando lo quiera cargar
    for x, y in siguiente_pieza:
        sig_pieza += f"{x}{y}"


    #  Escribo el archivo de guardado
    with open(ruta, "w") as archivo:
        archivo.write(f"{juego_aux}\n")
        archivo.write(f"{puntuacion}\n")
        archivo.write(f"{sig_pieza}")


def cargar_partida(ruta):
    """
    Carga la partida
    """
    nro_linea = 0
    juego = []
    sig_pieza = []
    # Primero cargo las variables
    with open(ruta, "r") as archivo:
        for linea in archivo:
            linea.rstrip()
            if nro_linea == 0:
                juego_aux = linea
            if nro_linea == 1:
                puntuacion = int(linea)
            if nro_linea == 2:
                sig_pieza_aux = linea
            nro_linea += 1

    # Reconstruimos la 'sig_pieza'
    cont_sig_pieza = 0
    pos_aux = []
    for valor in sig_pieza_aux:
        pos_aux.append(int(valor))
        cont_sig_pieza += 1
        if cont_sig_pieza == 2:
            sig_pieza.append(tuple(pos_aux))
            cont_sig_pieza = 0
            pos_aux = []

    # Reconstruimos el 'juego'
    fila_aux = []
    cont_juego = 0
    for ind, car in enumerate(juego_aux):
        if car == " ":
            fila_aux.append(CAR_VACIO)
        else:
            fila_aux.append(car)
        cont_juego += 1
        if cont_juego == ANCHO_JUEGO:
            juego.append(fila_aux)
            fila_aux = []
            cont_juego = 0

    return juego, puntuacion, tuple(sig_pieza)