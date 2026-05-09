import numpy as np
import scipy
import math
import pygame

#from scipy.constants import G as G

G = scipy.constants.G * 1e8
EPSILON_SOFTENING = 5e-3
N = 5

BODY_SIZE = 8
BODY_MASS = 1
INIT_SPEED = 0.3

SPEED_DECAY = 0.02
DECAY_TRESHOLD = 2.

SCREEN_SIZE = 720

WALL_FIELD_STRENGTH = 12
WALL_FIELD_EXPONENT = 8

POINT_FIELD_ENABLED = False
POINT_FIELD_STRENGTH = 0.4
POINT_FIELD_EPSILON_SOFTENING = 1e-1

POINTS_ON_LINE = 200

# coordinates

def cart2screen(x, y):
    return(
        SCREEN_SIZE/2 + x * SCREEN_SIZE/2,
        SCREEN_SIZE/2 - y * SCREEN_SIZE/2,
        )

def screen2cart(x, y):
    return (
        (x - SCREEN_SIZE/2) / (SCREEN_SIZE/2),
        (SCREEN_SIZE/2 - y) / (SCREEN_SIZE/2),
    )

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

# physics stuffs

def calcattractions(positions, masses):
    diff = positions[:, np.newaxis, :] - positions[np.newaxis, :, :]

    distances = np.linalg.norm(diff, axis=-1)

    with np.errstate(invalid='ignore'):
        unit = diff / distances[:, :, np.newaxis]
    unit[np.isnan(unit)] = 0

    with np.errstate(divide='ignore'):
        inv_sq = np.where(distances == 0, 0, 1 / (distances ** 2 + EPSILON_SOFTENING ** 2))

    inv_sq_weighted = inv_sq * masses[np.newaxis, :]

    accelerations = -G * (inv_sq_weighted[:, :, np.newaxis] * unit).sum(axis=1)

    return accelerations

# fields

def field(x, y):
    magnitude = math.sin(x**2 + y**2) ** WALL_FIELD_EXPONENT * WALL_FIELD_STRENGTH
    
    angle = cart2pol(x, y)[1] + math.pi
    
    return(
        pol2cart(magnitude, angle)
    )

def pointfield(x, y):
    mpos = screen2cart(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    mpos = np.array([mpos[0], mpos[1]])
    displacement = mpos - np.array([x,y])
    distance = np.linalg.norm(displacement)
    angle = cart2pol(displacement[0], displacement[1])[1]
    return(
        pol2cart(1/(distance + POINT_FIELD_EPSILON_SOFTENING**2)* POINT_FIELD_STRENGTH, angle)
    )