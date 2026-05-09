import pygame
import numpy as np
import math

import utils

from collections import deque

pygame.init()
screen = pygame.display.set_mode((utils.SCREEN_SIZE, utils.SCREEN_SIZE))
clock = pygame.time.Clock()
running = True

positions = np.zeros((utils.N, 2))
velocities = np.zeros((utils.N, 2))
masses = np.zeros(utils.N)

for i in range(0, utils.N):
    positions[i] = utils.pol2cart(0.5, i*(2*math.pi/utils.N))
    # velocities[i] = (np.zeros(2) - positions[i]) * utils.INIT_SPEED
    velocities[i] = utils.pol2cart(utils.INIT_SPEED, math.pi/2 + i*(2*math.pi/utils.N))
    masses[i] = utils.BODY_MASS

print(utils.field(0, 0))
print(utils.field(0.5,0))
print(utils.field(0.5, 0.5))

traces = []

for el in range(0, utils.N):
    traces.append(deque([]))
    for i in range(0, utils.POINTS_ON_LINE):
        traces[el].append(utils.cart2screen(positions[el][0],positions[el][1]))

while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                utils.POINT_FIELD_ENABLED = not utils.POINT_FIELD_ENABLED
                print(f"point field toggled: {utils.POINT_FIELD_ENABLED}")
        

    accelerations = utils.calcattractions(positions, masses)
    accelerations += np.array([utils.field(x, y) for x, y in positions])
    
    if utils.POINT_FIELD_ENABLED:
        accelerations += np.array([utils.pointfield(x, y) for x, y in positions])
    
    velocities += accelerations * dt
    for i in range(0, utils.N):
        if(np.linalg.norm(velocities[i]) >= utils.DECAY_TRESHOLD):
            velocities[i] *= (1 - utils.SPEED_DECAY)
    positions += velocities * dt

    screen.fill("black")

    for i in range(0, utils.N):
        traces[i].popleft()
        traces[i].append(utils.cart2screen(positions[i][0],positions[i][1]))
        #print(traces[i])
        pygame.draw.lines(screen, pygame.Color(80,80,80), False, traces[i], width=2)

    for i in range(0, utils.N):
        pos = pygame.Vector2(utils.cart2screen(positions[i][0], positions[i][1]))
        pygame.draw.circle(screen, "white", pos, utils.BODY_SIZE)

    
    pygame.display.flip()


pygame.quit()
