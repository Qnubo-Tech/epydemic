from enum import Enum

import numpy as np

from src.simulation import Time


class Status(Enum):
    Infected = "red"
    Immune = "darkgreen"
    Healthy = "blue"


class Disease:

    MEAN_TIME_TO_RECOVERY_IN_DAYS = 2
    TAU = MEAN_TIME_TO_RECOVERY_IN_DAYS * 24 * 60 * 60
    STD_TIME_TO_RECOVERY_IN_DAYS = 1
    TAU_STD = STD_TIME_TO_RECOVERY_IN_DAYS * 24 * 60 * 60

    def __init__(self, viral_load: float, radius: float):

        self.viral_load = viral_load
        self.infection_radius = radius
        self.tau = max(0, np.random.normal(loc=Disease.TAU, scale=Disease.TAU_STD))

        self.t_infected = 0

    def _update_infection_time(self, status: Status):

        if status == Status.Infected:
            self.t_infected += Time.STEP_SEC

    def _update_viral_load(self):

        if self.t_infected <= self.tau:
            self.viral_load *= 1
        else:
            self.viral_load *= 0

    def step(self, status: Status):

        self._update_infection_time(status=status)
        self._update_viral_load()

    def force(self, position: np.array, agent_position: np.array):

        return np.any(position != agent_position) * \
               (np.linalg.norm(position - agent_position) <= self.infection_radius) * \
               self.viral_load
