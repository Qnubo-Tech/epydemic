import numpy as np


class Box:
    Lx = 1
    Ly = 1

    @staticmethod
    def x_range():
        return np.linspace(0, Box.Lx, 100)

    @staticmethod
    def y_range():
        return np.linspace(0, Box.Ly, 100)

    @staticmethod
    def x_y():
        return np.meshgrid(Box.x_range(), Box.y_range())

    @staticmethod
    def x_limits():
        return [0, Box.Lx]

    @staticmethod
    def y_limits():
        return [0, Box.Ly]
