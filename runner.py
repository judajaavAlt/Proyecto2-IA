# Imports
import pygame
import random

# Setup the basics
pygame.init()
running = True
screen = [800, 800]
window = pygame.display.set_mode(screen)

# Creates the background
background = pygame.Surface([800, 800])
background.fill((235, 235, 208))

for i in range(8):
    for j in range(8):
        if (i % 2 == 0 and j % 2 != 0) or (i % 2 != 0 and j % 2 == 0):
            pygame.draw.rect(background,
                             (119, 148, 85), [i*100, j*100, 100, 100])

# define the points and horses positions
points = []

for v in range(1, 17):
    while True:
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        contains = any(item[0] == [x, y] for item in points)
        if not contains:
            if v <= 10:
                img = pygame.image.load(f"{v}.png")
                value = int(v)
            elif v <= 14:
                value = "x2"
                img = pygame.image.load("X2.png")
            elif v == 15:
                value = "white_horse"
                img = pygame.image.load("white_horse.png")
            else:
                value = "black_horse"
                img = pygame.image.load("black_horse.png")
            print(value)
            if value != "white_horse" and value != "black_horse":
                points.append([[x, y], value, img])
            else:
                if value == "white_horse":
                    white_horse = [[x, y], img]
                else:
                    black_horse = [[x, y], img]
            break


# Game cycle
while running:
    window.blit(background, [0, 0])

    for point in points:
        [x, y], _, image = point
        position = [x*100, y*100]
        window.blit(image, position)

    [x, y], image = white_horse
    window.blit(image, [x*100, y*100])
    [x, y], image = black_horse
    window.blit(image, [x*100, y*100])

    pygame.display.update()

# Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Game finish
pygame.quit()
