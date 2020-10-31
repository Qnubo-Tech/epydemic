import numpy as np


class Geometry:

    class Box:
        Lx = 1
        Ly = 1

        @staticmethod
        def x_range():
            return np.linspace(0, Geometry.Box.Lx, 100)

        @staticmethod
        def y_range():
            return np.linspace(0, Geometry.Box.Ly, 100)

        @staticmethod
        def x_y():
            return np.meshgrid(Geometry.Box.x_range(),
                               Geometry.Box.y_range())

        @staticmethod
        def x_limits():
            return [0, Geometry.Box.Lx]

        @staticmethod
        def y_limits():
            return [0, Geometry.Box.Ly]
