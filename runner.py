# Imports
import random
import math
import tkinter
import pygame


def launch(white_IA=None, black_IA=None):
    # Initialize pygame
    pygame.init()

    # Setup the window
    screen_height = pygame.display.get_desktop_sizes()[0][1]*0.8
    cell_size = math.trunc(screen_height/9)
    screen = [cell_size*8, cell_size*9]
    window = pygame.display.set_mode(screen, display=0)

    # define basics
    scale = screen[1]/900
    running = True
    font = pygame.font.Font(size=round(80*scale))
    is_white_turn = True

    # Load the sprites
    spriteSheet = pygame.image.load("spriteSheet.png")
    sprites = []
    for y in range(7):
        for x in range(2):
            sprite = spriteSheet.subsurface([x*100, y*100, 100, 100])
            sprites.append(pygame.transform.smoothscale_by(sprite, scale))

    # Creates the background

    background = pygame.Surface(screen)
    background.fill((235, 235, 208))
    for i in range(8):
        for j in range(8):
            if (i % 2 == 0 and j % 2 != 0) or (i % 2 != 0 and j % 2 == 0):
                pygame.draw.rect(background,
                                 (119, 148, 85),
                                 [i*100*scale,
                                  j*100*scale,
                                  100*scale,
                                  100*scale])
    pygame.draw.rect(background,
                     (200, 200, 220),
                     [0, 800*scale, 800*scale, 100*scale])

    # Min-max solver
    # heuristic must be a lambda expression
    def do_min_max(deepth, heuristic, white_position,
                   black_position, is_white_turn, white_points,
                   black_points, white_has_bonus, black_has_bonus,
                   points, is_white):

        heuristic = heuristic(white_points, black_points)
        # Creates the three
        tree = Node(white_position, black_position, is_white_turn,
                    white_points, black_points, white_has_bonus,
                    black_has_bonus, points)
        actual_node = tree

        # Ciclo de expansion y poda
        while True:
            print(actual_node.white_position)
            print(actual_node.points)
            has_parent_ref = (actual_node.parent.valor is not None if
                              actual_node.parent is not None else False)
            # Primera vez expansion
            if (actual_node.profundidad < deepth and
                    actual_node.hijos == []):
                actual_node.expandir()
                actual_node = actual_node.hijos[0]
                pass

            # Hoja
            elif actual_node.profundidad == deepth:
                white_points = actual_node.white_points
                black_points = actual_node.black_points
                white_has_bonus = actual_node.white_has_bonus
                black_has_bonus = actual_node.black_has_bonus
                actual_node.valor = heuristic(white_points, black_points,
                                              white_has_bonus, black_has_bonus)
                actual_node = actual_node.parent
                pass

            # poda
            elif actual_node.hijos != [] and not has_parent_ref:
                sons = actual_node.hijos
                did_heuristic = [node for node in sons if node.valor is None]

                values = [node.valor for node in sons
                          if node.valor is not None]
                if actual_node.is_min:
                    actual_node.valor = sorted(values)[0]
                else:
                    actual_node.valor = sorted(values, reverse=True)[0]

                if len(did_heuristic) > 0:
                    actual_node = did_heuristic[0]
                else:
                    if actual_node.parent is None:
                        break
                    actual_node = actual_node.parent
                pass

            elif actual_node.hijos != [] and has_parent_ref:
                sons = actual_node.hijos
                did_heuristic = [node for node in sons if node.valor is None]

                values = [node.valor for node in sons
                          if node.valor is not None]
                if actual_node.is_min:
                    actual_node.valor = sorted(values)[0]
                else:
                    actual_node.valor = sorted(values, reverse=True)[0]

                if actual_node.parent.is_min:
                    if actual_node.parent.valor <= actual_node.valor:
                        actual_node = actual_node.parent
                else:
                    if actual_node.parent.valor >= actual_node.valor:
                        actual_node = actual_node.parent

                if len(did_heuristic) > 0:
                    actual_node = did_heuristic[0]
                else:
                    actual_node = actual_node.parent
                pass

        def sort_by_value(node):
            return node.valor
        if tree.is_min:
            node = sorted(tree.hijos, key=sort_by_value)[0]
            if is_white:
                position = node.white_position
            else:
                position = node.black_position
        else:
            node = sorted(tree.hijos, key=sort_by_value, reversed=True)[0]
            if is_white:
                position = node.white_position
            else:
                position = node.black_position

        return position

    # Define the classes
    class Point:
        def __init__(self, position, value, image):
            self.position = position
            self.value = value
            self.image = image

        def __str__(self):
            return f"i'm the point {self.value} positioned at {self.position}"

        def render(self):
            x, y = self.position
            position = [x*100*scale, y*100*scale]
            window.blit(self.image, position)

    class Node:  # Clase del nodo
        def __init__(self, white_position, black_position, is_white_turn,
                     white_points, black_points, white_has_bonus,
                     black_has_bonus, points,
                     profundidad=0, hijos=[], parent=None, is_min=False):
            # Guarda la información de los caballos
            self.white_position = white_position
            self.black_position = black_position
            self.is_white_turn = is_white_turn
            self.white_points = white_points
            self.black_points = black_points
            self.white_has_bonus = white_has_bonus
            self.black_has_bonus = black_has_bonus
            self.points = points
            self.profundidad = profundidad  # indica a que profundidad del nodo
            self.parent = parent
            self.valor = None  # heuristica
            self.is_min = is_min  # determina si es min o max
            # Lista de hijos la cual representa la cantidad
            #  de movimientos disponibles
            self.hijos = hijos

        def get_movements(self, position, enemy_pos):
            possible_movements = []

            if position[1] >= 2:
                if position[0] >= 1:  # UL
                    possible_movements.append([position[0] - 1,
                                               position[1] - 2])
                if position[0] <= 6:  # UR
                    possible_movements.append([position[0] + 1,
                                               position[1] - 2])
            if position[1] <= 5:
                if position[0] >= 1:  # DL
                    possible_movements.append([position[0] - 1,
                                               position[1] + 2])
                if position[0] <= 6:  # DR
                    possible_movements.append([position[0] + 1,
                                               position[1] + 2])
            if position[0] >= 2:
                if position[1] >= 1:  # LU
                    possible_movements.append([position[0] - 2,
                                               position[1] - 1])
                if position[1] <= 6:  # LD
                    possible_movements.append([position[0] - 2,
                                               position[1] + 1])
            if position[0] <= 5:
                if position[1] >= 1:  # RU
                    possible_movements.append([position[0] + 2,
                                               position[1] - 1])
                if position[1] <= 6:  # RD
                    possible_movements.append([position[0] + 2,
                                               position[1] + 1])

            if enemy_pos in possible_movements:
                possible_movements.remove(enemy_pos)

            return possible_movements

        def move_horse(self, position, total_points, points, has_x2):
            for point in points:
                if point.position == position:
                    if point.value != "x2":
                        if has_x2:
                            total_points += int(point.value) * 2
                            has_x2 = False
                        else:
                            total_points += int(point.value)
                        new_points = [item for item in points if item == point]
                    elif not has_x2:
                        has_x2 = True
                        new_points = [item for item in points if item == point]
                else:
                    new_points = points

            return [total_points, has_x2, new_points]

        # def expandir() esta función primero comprueba con que caballo
        # esta trabajando le dice que movimiento puede tener,
        # utiliza el move_horse para saber, que efecto tendria ese movimiento
        # y genera un hijo por cada movimiento
        def expandir(self):
            # Verifica a cual caballo corresponde el turno actual
            if self.is_white_turn:
                # Verifica los movimientos disponibles
                possible_moves = self.get_movements(self.white_position,
                                                    self.black_position)
                # Ejecuta el movimiento y lo guarda en un nuevo nodo
                for move in possible_moves:
                    new_total_points, new_has_x2, new_points = self.move_horse(
                        move,
                        self.white_points,
                        self.points,
                        self.white_has_bonus)

                    # Crea un nodo nuevo con la información del movimiento
                    nuevo_nodo = Node(
                        white_position=move,
                        black_position=self.black_position,
                        is_white_turn=not self.is_white_turn,
                        white_points=new_total_points,
                        black_points=self.black_points,
                        points=new_points,
                        white_has_bonus=new_has_x2,
                        black_has_bonus=self.black_has_bonus,
                        profundidad=self.profundidad + 1,
                        parent=self,
                        is_min=not self.is_min,
                        hijos=[],
                    )
                    self.hijos.append(nuevo_nodo)
            else:
                possible_moves = self.get_movements(self.black_position,
                                                    self.white_position)
                for move in possible_moves:
                    new_total_points, new_has_x2, new_points = self.move_horse(
                        move,
                        self.black_points,
                        self.points,
                        self.black_has_bonus)

                    # Crea un nodo nuevo con la información del movimiento
                    nuevo_nodo = Node(
                        white_position=self.white_position,
                        black_position=move,
                        is_white_turn=not self.is_white_turn,
                        white_points=self.white_points,
                        black_points=new_total_points,
                        points=new_points,
                        white_has_bonus=self.white_has_bonus,
                        black_has_bonus=new_has_x2,
                        profundidad=self.profundidad + 1,
                        parent=self,
                        is_min=not self.is_min,
                        hijos=[],
                    )
                    self.hijos.append(nuevo_nodo)
            # Guarda el nuevo nodo como hijo

    class Horse:
        def __init__(self, is_white, position, image, ia):
            self.is_white = is_white
            self.position = position
            self.image = image
            self.is_ia = ia is not None
            self.ia = ia
            self.has_x2 = False
            self.points = 0

        def __str__(self):
            string = f"{"S" if self.is_white else "No S"}oy el caballo blanco"
            string += f", estoy en la posicion {self.position}"
            return string

        def render_moves(self, expected_position=None):
            def setPosition(position):
                return [position[0]*100*scale, position[1]*100*scale]

            possible_movements = []
            if expected_position is None:
                position = self.position
            else:
                position = expected_position

            if position[1] >= 2:
                if position[0] >= 1:  # UL
                    possible_movements.append([position[0] - 1,
                                               position[1] - 2])
                if position[0] <= 6:  # UR
                    possible_movements.append([position[0] + 1,
                                               position[1] - 2])
            if position[1] <= 5:
                if position[0] >= 1:  # DL
                    possible_movements.append([position[0] - 1,
                                               position[1] + 2])
                if position[0] <= 6:  # DR
                    possible_movements.append([position[0] + 1,
                                               position[1] + 2])
            if position[0] >= 2:
                if position[1] >= 1:  # LU
                    possible_movements.append([position[0] - 2,
                                               position[1] - 1])
                if position[1] <= 6:  # LD
                    possible_movements.append([position[0] - 2,
                                               position[1] + 1])
            if position[0] <= 5:
                if position[1] >= 1:  # RU
                    possible_movements.append([position[0] + 2,
                                               position[1] - 1])
                if position[1] <= 6:  # RD
                    possible_movements.append([position[0] + 2,
                                               position[1] + 1])

            square = pygame.Surface([100*scale, 100*scale])
            square.fill((66, 188, 245))
            if self.is_white:
                enemy_pos = black_horse.position
            else:
                enemy_pos = white_horse.position

            if enemy_pos in possible_movements:
                possible_movements.remove(enemy_pos)

            if not self.is_ia:
                for position in possible_movements:
                    window.blit(square,
                                setPosition(position) + [100*scale, 100*scale])
                    window.blit(square,
                                (setPosition(self.position) +
                                 [100*scale, 100*scale]))
            return possible_movements

        def render(self):
            x, y = self.position
            position = [x*100*scale, y*100*scale]
            window.blit(self.image, position)

        def decide_by_ia(self, is_white_turn, points,
                         enemy_position,
                         enemy_points,
                         enemy_has_bonus):
            if self.is_white:
                def heuristic(white_points_init, black_points_init):
                    def new_heuristic(white_points, black_points,
                                      white_has_bonus, black_has_bonus):
                        puntuacion_final_w = white_points_init - white_points
                        puntuacion_final_w += 1 if white_has_bonus else 0
                        puntuacion_final_b = black_points_init - black_points
                        puntuacion_final_b += 1 if black_has_bonus else 0
                        return puntuacion_final_w - puntuacion_final_b
                    return new_heuristic
            else:
                def heuristic():
                    pass
            self_position = self.position
            self_points = self.points
            self_has_bonus = self.has_x2
            do_min_max(int(self.ia), heuristic, self_position,
                       enemy_position, is_white_turn, self_points,
                       enemy_points, self_has_bonus, enemy_has_bonus,
                       points, self.is_white)
            return self.position

        def move(self, position, points):
            self.position = position
            for point in points:
                if point.position == position:
                    if point.value != "x2":
                        if self.has_x2:
                            self.points += int(point.value) * 2
                            self.has_x2 = False
                        else:
                            self.points += int(point.value)
                        points.remove(point)
                    elif not self.has_x2:
                        self.has_x2 = True
                        points.remove(point)

    # define the points and horses positions

    used_positions = []
    points = []
    for v in range(1, 17):
        while True:
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            contains = any(item == [x, y] for item in used_positions)
            if not contains:
                if v <= 10:
                    image = sprites[v - 1]
                    value = int(v)
                elif v <= 14:
                    image = sprites[10]
                    value = "x2"
                elif v == 15:
                    value = "white_horse"
                    image = sprites[11]
                else:
                    value = "black_horse"
                    image = sprites[12]
                if value != "white_horse" and value != "black_horse":
                    points.append(Point([x, y], value, image))
                else:
                    if value == "white_horse":
                        white_horse = Horse(True,
                                            [x, y],
                                            image,
                                            white_IA)
                    else:
                        black_horse = Horse(False,
                                            [x, y],
                                            image,
                                            black_IA)
                used_positions.append([x, y])
                break

    print("first pos:", white_horse.position)

    # Game cycle
    while running:
        text = None
        window.blit(background, [0, 0])
        points_without_x2 = [item for item in points if item.value != "x2"]
        is_game_continuing = len(list(points_without_x2)) > 0

        if is_game_continuing:
            if is_white_turn:
                if white_horse.is_ia:
                    decision = white_horse.decide_by_ia(is_white_turn, points,
                                                        black_horse.position,
                                                        black_horse.points,
                                                        black_horse.has_x2)
                    white_horse.move(decision, points)
                    is_white_turn = False
                else:
                    moves = white_horse.render_moves()
            else:
                if black_horse.is_ia:
                    decision = black_horse.decide_by_ia(is_white_turn, points,
                                                        white_horse.position,
                                                        white_horse.points,
                                                        white_horse.has_x2)
                    black_horse.move(decision, points)
                    is_white_turn = True
                else:
                    moves = black_horse.render_moves()
            # puntos en pantalla
            for point in points:
                point.render()
        else:
            window.blit(background, [0, 0])
            win_font = pygame.font.Font(size=round(200*scale))
            star_position = None
            if white_horse.points > black_horse.points:
                text = win_font.render("White wins", True, (0, 0, 0))
                x, y = white_horse.position
            elif white_horse.points < black_horse.points:
                text = win_font.render("Black wins", True, (0, 0, 0))
                x, y = black_horse.position
            else:
                text = win_font.render("Draw", True, (0, 0, 0))

            w, h = text.get_size()
            sw, _ = screen
            text.set_alpha(250)
            text_position = [sw/2 - w/2, 800*scale/2 - h/2]

            if white_horse.points != black_horse.points:
                star_position = [x*100*scale, y*100*scale]
                window.blit(sprites[13], star_position)

        # puntaje
        points_text = font.render(f"{white_horse.points}", True, (0, 0, 0))
        _, h = points_text.get_size()
        if white_horse.has_x2:
            window.blit(sprites[10], [130*scale, 800*scale])
        window.blit(sprites[11], [200*scale, 800*scale])
        window.blit(points_text, [280*scale, 850*scale - h/2])

        points_text = font.render(f"{black_horse.points}", True, (0, 0, 0))
        w, h = points_text.get_size()
        if black_horse.has_x2:
            window.blit(sprites[10], [570*scale, 800*scale])
        window.blit(sprites[12], [500*scale, 800*scale])
        window.blit(points_text, [500*scale - w, 850*scale - h/2])
        # caballos
        white_horse.render()
        black_horse.render()

        if text is not None:
            window.blit(text, text_position)

        pygame.display.update()

    # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif is_game_continuing:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    position = [math.trunc(x/cell_size),
                                math.trunc(y/cell_size)]
                    if position in moves:
                        if is_white_turn and not white_horse.is_ia:
                            white_horse.move(position, points)
                            is_white_turn = False
                        elif not is_white_turn and not black_horse.is_ia:
                            black_horse.move(position, points)
                            is_white_turn = True

    # Game finish
    pygame.quit()
    launch_menu()


def launch_menu():
    # crea la ventana
    root = tkinter.Tk()

    # define las caracteristicas de la ventana
    screen_size = [root.winfo_screenwidth(), root.winfo_screenheight()]
    interface_size = [300, 360]
    margins = f"{int((screen_size[0] - interface_size[0]) / 2)}"
    margins += f"+{int((screen_size[1] - interface_size[1]) / 2)}"
    geometry = f'{interface_size[0]}x{interface_size[1]}+{margins}'
    root.title('Smart Horses launcher')
    root.geometry(geometry)

    frame = tkinter.Frame(root)
    frame.pack()
    # elige el modo de juego
    label_game_mode = tkinter.Label(frame, text='Elige el modo de juego')
    label_game_mode.grid(column=0, row=0, sticky='w')

    variable_modo = tkinter.StringVar()
    variable_modo.set("pvp")

    radio_pvp = tkinter.Radiobutton(frame,
                                    text='Jugador vs Jugador',
                                    value='pvp',
                                    variable=variable_modo)
    radio_pvp.grid(column=0, row=1, sticky='w')

    radio_pve = tkinter.Radiobutton(frame,
                                    text='Jugador vs IA',
                                    value='pve',
                                    variable=variable_modo)
    radio_pve.grid(column=0, row=2, sticky='w')

    radio_eve = tkinter.Radiobutton(frame,
                                    text='IA vs IA',
                                    value='eve',
                                    variable=variable_modo)
    radio_eve.grid(column=0, row=3, sticky='w')

    # elige la dificultad de la IA
    label_IA_w = tkinter.Label(frame, text='Elige la IA')
    variable_IA_w = tkinter.StringVar()
    variable_IA_w.set("2")

    radio_easy_w = tkinter.Radiobutton(frame,
                                       text='Facil',
                                       value='2',
                                       variable=variable_IA_w)
    radio_mid_w = tkinter.Radiobutton(frame,
                                      text='Medio',
                                      value='4',
                                      variable=variable_IA_w)
    radio_hard_w = tkinter.Radiobutton(frame,
                                       text='Dificil',
                                       value='6',
                                       variable=variable_IA_w)

    # elige la dificultad de la segunda IA
    label_IA_b = tkinter.Label(frame, text='Elige la segunda IA')
    variable_IA_b = tkinter.StringVar()
    variable_IA_b.set("2")

    radio_easy_b = tkinter.Radiobutton(frame,
                                       text='Facil',
                                       value='2',
                                       variable=variable_IA_b)
    radio_mid_b = tkinter.Radiobutton(frame,
                                      text='Medio',
                                      value='4',
                                      variable=variable_IA_b)
    radio_hard_b = tkinter.Radiobutton(frame,
                                       text='Dificil',
                                       value='6',
                                       variable=variable_IA_b)

    # define el boton de iniciar

    def close_and_launch():
        global running
        running = False
        root.destroy()
        if variable_modo.get() == "pvp":
            launch()
        elif variable_modo.get() == "pve":
            launch(variable_IA_w.get())
        else:
            launch(variable_IA_w.get(), variable_IA_b.get())

    button_start = tkinter.Button(frame,
                                  text='Iniciar juego',
                                  command=close_and_launch)
    button_start.grid(column=0, row=13, sticky='nsew', pady=10)

    # corre la ventana
    running = True

    # define la funcion para cerrar el programa
    def on_close():
        global running
        running = False
        root.destroy()

    # define el loop de menu
    while running:
        if variable_modo.get() == "pve" or variable_modo.get() == "eve":
            label_IA_w.grid(column=0, row=4, sticky='w')
            radio_easy_w.grid(column=0, row=5, sticky='w')
            radio_mid_w.grid(column=0, row=6, sticky='w')
            radio_hard_w.grid(column=0, row=7, sticky='w')
        else:
            label_IA_w.grid_forget()
            radio_easy_w.grid_forget()
            radio_mid_w.grid_forget()
            radio_hard_w.grid_forget()

        if variable_modo.get() == "eve":
            label_IA_b.grid(column=0, row=8, sticky='w')
            radio_easy_b.grid(column=0, row=9, sticky='w')
            radio_mid_b.grid(column=0, row=10, sticky='w')
            radio_hard_b.grid(column=0, row=11, sticky='w')
        else:
            label_IA_b.grid_forget()
            radio_easy_b.grid_forget()
            radio_mid_b.grid_forget()
            radio_hard_b.grid_forget()
        root.protocol("WM_DELETE_WINDOW", on_close)
        root.update_idletasks()
        root.update()


launch_menu()
'''
Profundidad: {self.profundidad}"""
                if node.valor > 0:
                    result += f"\nEl valor de la solucion es: {node.valor}"
                return [result, node.pasos]
            # en caso de no encontrar la meta, expandira el nodo creando hijos
            else:
                y = node.posicion[0]  # define la posicion en y del nodo padre
                x = node.posicion[1]  # define la posicion en x del nodo padre
                # se define la profundidad de los nuevos nodos
                profundidad = node.profundidad + 1
                # si el nuevo nodo es el mas profundo, se aumenta la
                # profundidad total del arbol
                if profundidad > self.profundidad:
                    self.profundidad = profundidad
                # se comprueba si es la casilla del pasajero
                es_pasajero = node.posicion == self.pasajero
                # se comprueba si lleva el pasajero o lo acaba de recoger
                tiene_pasajero = (es_pasajero or
                                  node.tiene_pasajero)
                # se obtiene el paso previo a llegar al nodo padre
                last_step = node.pasos[-1] if len(node.pasos) > 0 else ''
'''
