import numpy as np

N = 13
BODY_SIZE = 15
SCREEN_SIZE = 720

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
