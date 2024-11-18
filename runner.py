# Imports
import pygame
import random

# Setup the basics
pygame.init()
running = True
screen = [800, 800]
window = pygame.display.set_mode(screen)
escene = 0

# Load the sprites
spriteSheet = pygame.image.load("spriteSheet.png")
sprites = []
for y in range(7):
    for x in range(2):
        sprites.append(spriteSheet.subsurface([x*100, y*100, 100, 100]))
sprites.pop(-1)

# Creates the background

background = pygame.Surface([800, 800])
background.fill((235, 235, 208))
for i in range(8):
    for j in range(8):
        if (i % 2 == 0 and j % 2 != 0) or (i % 2 != 0 and j % 2 == 0):
            pygame.draw.rect(background,
                             (119, 148, 85), [i*100, j*100, 100, 100])


# Define the classes
class Point:
    def __init__(self, position, value, image):
        self.position = position
        self.value = value
        self.image = image

    def __str__(self):
        print(f"i'm the point {self.value} positioned at {self.position}")

    def get_position(self):
        x, y = self.position
        return [x*100, y*100]

    def render(self):
        window.blit(self.image, self.get_position())


class Horse:
    def __init__(self, is_white, position, image):
        self.is_white = is_white
        self.position = position
        self.image = image

    def __str__(self):
        string = f"{"S" if self.is_white else "No S"}oy el caballo blanco"
        string += f", estoy en la posicion {self.position}"
        print(string)

    def render_moves(self):
        def setPosition(position):
            return [position[0] * 100, position[1] * 100]

        possible_movements = []
        position = self.position

        if position[1] >= 2:
            if position[0] >= 1:  # UL
                possible_movements.append([position[0] - 1, position[1] - 2])
            if position[0] <= 6:  # UR
                possible_movements.append([position[0] + 1, position[1] - 2])
        if position[1] <= 5:
            if position[0] >= 1:  # DL
                possible_movements.append([position[0] - 1, position[1] + 2])
            if position[0] <= 6:  # DR
                possible_movements.append([position[0] + 1, position[1] + 2])
        if position[0] >= 2:
            if position[1] >= 1:  # LU
                possible_movements.append([position[0] - 2, position[1] - 1])
            if position[1] <= 6:  # LD
                possible_movements.append([position[0] - 2, position[1] + 1])
        if position[0] <= 5:
            if position[1] >= 1:  # RU
                possible_movements.append([position[0] + 2, position[1] - 1])
            if position[1] <= 6:  # RD
                possible_movements.append([position[0] + 2, position[1] + 1])

        square = pygame.Surface([100, 100])
        square.fill((66, 188, 245))
        print(possible_movements)
        for position in possible_movements:
            window.blit(square, setPosition(position) + [100, 100])
        return possible_movements

    def render(self):
        window.blit(self.image, self.get_position())

    def get_position(self):
        x, y = self.position
        return [x*100, y*100]


class Button:
    def __init__(self, position, size, func):
        self.position = position
        self.size = size
        self.func = func(self)
        self.color = (255, 0, 0)

    def render(self):
        pygame.draw.rect(window, self.color, self.position + self.size)


# define the points and horses positions
def set_scenario():
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
                        white_horse = Horse(True, [x, y], image)
                    else:
                        black_horse = Horse(False, [x, y], image)
                used_positions.append([x, y])
                break
    return [points, white_horse, black_horse]


points, white_horse, black_horse = set_scenario()

# Game cycle
while running:
    if escene == 0:
        window.fill((200, 200, 220))
    elif escene == 1:
        window.blit(background, [0, 0])
        for point in points:
            point.render()

        white_horse.render()
        black_horse.render()

    pygame.display.update()

# Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Game finish
pygame.quit()
