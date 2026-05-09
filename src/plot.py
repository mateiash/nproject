import numpy as np
import matplotlib.pyplot as plt
import utils

x = np.linspace(-1, 1, 30)
y = np.linspace(-1, 1, 30)
X, Y = np.meshgrid(x, y)

vx, vy = np.vectorize(utils.field)(X, Y)

plt.figure(figsize=(6, 6))
plt.quiver(X, Y, vx, vy)
plt.savefig("plot.png")
plt.show()