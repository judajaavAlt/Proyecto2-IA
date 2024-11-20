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

        def decide_by_ia(self):
            x = self.render_moves()
            return x[0]

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

    # Game cycle
    while running:
        text = None
        window.blit(background, [0, 0])
        points_without_x2 = [item for item in points if item.value != "x2"]
        is_game_continuing = len(list(points_without_x2)) > 0

        if is_game_continuing:
            if is_white_turn:
                if white_horse.is_ia:
                    decision = white_horse.decide_by_ia()
                    white_horse.move(decision, points)
                    is_white_turn = False
                else:
                    moves = white_horse.render_moves()
            else:
                if black_horse.is_ia:
                    decision = black_horse.decide_by_ia()
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
