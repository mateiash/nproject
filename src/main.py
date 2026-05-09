import pygame
import numpy as np
import math

import utils

pygame.init()
screen = pygame.display.set_mode((utils.SCREEN_SIZE, utils.SCREEN_SIZE))
clock = pygame.time.Clock()
running = True

positions = np.zeros((utils.N, 2))
velocities = np.zeros((utils.N, 2))

for i in range(0, utils.N):
    positions[i] = utils.pol2cart(0.5, i*(2*math.pi/utils.N))

print("positions")
print(positions)

while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    for i in range(0, utils.N):
        pos = pygame.Vector2(utils.cart2screen(positions[i][0], positions[i][1]))
        pygame.draw.circle(screen, "white", pos, utils.BODY_SIZE)

    pygame.display.flip()


pygame.quit()
