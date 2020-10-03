from enum import Enum

import numpy as np

TIMESTEP_SEC = 3600
TIMESTEP_MIN = TIMESTEP_SEC / 60
TAU = 14*24*60*60


class Geometry:

    class Box:
        Lx = 1
        Ly = 1
        x_range = np.linspace(0, Lx, 100)
        y_range = np.linspace(0, Ly, 100)
        X, Y = np.meshgrid(x_range, y_range)
        x_lims = [0, Lx]
        y_lims = [0, Ly]


class Status(Enum):
    Infected = "red"
    Immune = "darkgreen"
    Helathy = "blue"


class Agent:

    def __init__(self, x, y, radius: float, status: Status, mobility: float):

        self.position = np.array([x, y])
        self.infection_radius = radius

        self.status = status
        self.t_infected = 0
        self.viral_load = self._set_viral_load()

        self.mobility = mobility

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    def _set_viral_load(self):

        if self.status == Status.Infected:
            return 1
        else:
            return 0

    def _update_position(self):

        return np.random.normal(0, self.mobility * TIMESTEP_SEC, size=2)

    def _apply_boundary_conditions(self):

        self.position = self.position % np.array([Geometry.Box.Lx, Geometry.Box.Ly])

    def _update_infection_time(self):

        if self.status == Status.Infected:
            self.t_infected += TIMESTEP_SEC

    def _update_viral_load(self):

        self.viral_load *= 1 if self.t_infected <= TAU else 0

    def step(self):

        self.position += self._update_position()
        self._apply_boundary_conditions()

        self._update_infection_time()
        self._update_viral_load()

    def viral_force(self, position):

        #return ((np.linalg.norm(position - self.position) <= self.infection_radius) and
        #        any(position != self.position)) * self.viral_load

        return any(position != self.position) * (1 / (1 + np.exp(-10*np.linalg.norm(position - self.position)))) * self.viral_load

