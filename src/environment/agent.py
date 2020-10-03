import numpy as np

from src.geometry import Geometry
from src.environment.disease import Disease, Status
from src.simulation import Time


class Agent:

    def __init__(self, x: float, y: float, mobility: float, status: Status):

        self.position = np.array([x, y])
        self.mobility = mobility

        self.status = status
        initial_viral_load = self._set_initial_viral_load()
        self.disease = Disease(viral_load=initial_viral_load, radius=0.02)

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    @property
    def viral_load(self):
        return self.disease.viral_load

    def _set_initial_viral_load(self):
        return 1 if self.status == Status.Infected else 0

    def _update_position(self):

        return np.random.normal(0, self.mobility * Time.STEP_SEC, size=2)

    def _apply_boundary_conditions(self):

        self.position = self.position % np.array([Geometry.Box.Lx, Geometry.Box.Ly])

    def step(self, force):
        self.position += self._update_position()
        self._apply_boundary_conditions()
        self.status = self.disease.step(status=self.status, force=force)

    def viral_force(self, position):

        return self.disease.force(position=position, agent_position=self.position)

