import numpy as np

from src.geometry import Box
from src.environment.disease import Disease, Immunity, Infection
from src.environment.mobility import MobilityFactory, MobilityType
from src.environment.status import Status
from src.configuration import Time, DiseaseParams


class Agent:

    def __init__(self,
                 x: float,
                 y: float,
                 mobility_value: float,
                 mobility_type: MobilityType,
                 status: Status):

        self.position = np.array([x, y])
        self.mobility = MobilityFactory.build(mobility_type=mobility_type,
                                              initial_value=mobility_value)

        self.status = status
        initial_viral_load = self._set_initial_viral_load()
        self.disease = Disease(viral_load=initial_viral_load,
                               radius=DiseaseParams.INFECTION_RADIUS,
                               immunity=Immunity(),
                               infection=Infection())

        self.allow_confinement = False

        self.t_alive = 0

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    @property
    def viral_load(self):
        return self.disease.viral_load

    @property
    def mobility_args(self):
        return {"time_alive": self.t_alive}

    def _set_initial_viral_load(self):
        return 1 if self.status == Status.Infected else 0

    def _check_confinement(self):
        if self.allow_confinement and self.status == Status.Infected:
            self.status = Status.Confined

    def _apply_boundary_conditions(self):
        self.position = self.position % np.array([Box.Lx, Box.Ly])

    def step(self, force):
        self.status = self.disease.step(status=self.status, force=force)
        self.mobility.update_value(status=self.status)

        self._check_confinement()

        if self.status != Status.Confined:
            self.position += self.mobility.update_position(mobility_args=self.mobility_args)
            self._apply_boundary_conditions()
        else:
            self.position = np.array([-1.0, -1.0])

        self.t_alive += Time.STEP_SEC

    def viral_force(self, position):

        return self.disease.force(position=position, agent_position=self.position)

