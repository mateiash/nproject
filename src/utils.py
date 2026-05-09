import numpy as np
import scipy

#from scipy.constants import G as G

G = scipy.constants.G * 1e8

N = 18

BODY_SIZE = 15
BODY_MASS = 1

SCREEN_SIZE = 720
INIT_SPEED = 0.1

POINTS_ON_LINE = 450

def cart2screen(x, y):
    return(
        SCREEN_SIZE/2 + x * SCREEN_SIZE/2,
        SCREEN_SIZE/2 - y * SCREEN_SIZE/2,
        )

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

def calcattractions(positions, masses):
    diff = positions[:, np.newaxis, :] - positions[np.newaxis, :, :]

    distances = np.linalg.norm(diff, axis=-1)

    with np.errstate(invalid='ignore'):
        unit = diff / distances[:, :, np.newaxis]
    unit[np.isnan(unit)] = 0

    with np.errstate(divide='ignore'):
        inv_sq = np.where(distances == 0, 0, 1 / distances ** 2)

    inv_sq_weighted = inv_sq * masses[np.newaxis, :]

    accelerations = -G * (inv_sq_weighted[:, :, np.newaxis] * unit).sum(axis=1)

    return accelerations