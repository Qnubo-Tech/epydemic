import numpy as np


class Geometry:

    class Box:
        Lx = 1
        Ly = 1
        x_range = np.linspace(0, Lx, 100)
        y_range = np.linspace(0, Ly, 100)
        X, Y = np.meshgrid(x_range, y_range)
        x_limits = [0, Lx]
        y_limits = [0, Ly]
