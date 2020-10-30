import numpy as np

from src.environment.status import Status

from src.simulation import DiseaseParams

from src.environment.disease.immunity import Immunity
from src.environment.disease.infection import Infection


class Disease:

    def __init__(self, viral_load: float, radius: float, immunity: Immunity, infection: Infection):

        self.viral_load = viral_load
        self.infection_radius = radius

        self.immunity = immunity
        self.infection = infection

    def _update_times(self, status: Status):

        if (status == Status.Infected) or (status == Status.Confined):
            self.infection.update_time()
        if status == Status.Immune:
            self.immunity.update_time()

    def _keep_viral_load(self):
        self.viral_load *= 1

    def _unload_viral_load(self):
        self.viral_load *= np.exp(-DiseaseParams.VIRAL_UNLOADING_RATE)

    def _increase_viral_load(self, force: float):
        self.viral_load += DiseaseParams.VIRAL_STICKINESS * force
        self.viral_load = min(self.viral_load, 1.0)

    def _update_dynamics(self, status: Status, force: float):

        if status == Status.Infected:

            if self.infection.time <= self.infection.duration:
                self._keep_viral_load()
                return self.infection.check_confinement()

            else:
                self._unload_viral_load()
                return self.infection.check_recovery()

        if status == Status.Healthy:
            # Getting some infection:
            if force != 0:
                self._increase_viral_load(force=force)

            # Unloading because it left the dangerous region:
            else:
                self._unload_viral_load()

            # Is it already infected?:
            if self.viral_load > DiseaseParams.VIRAL_LOAD_INFECTION_THRESHOLD:
                return Status.Infected

            # It's still healthy:
            return status

        if status == Status.Immune:
            self._unload_viral_load()

            if self.immunity.time > self.immunity.duration:
                return self.immunity.check_immunity_loss()

            else:
                return status

        if status == Status.Confined:
            self._unload_viral_load()

            if self.infection.time > self.infection.duration:
                return self.infection.check_recovery()

            else:
                return status

    def step(self, status: Status, force: float):

        self._update_times(status=status)
        new_status = self._update_dynamics(status=status, force=force)
        return new_status

    def force(self, position: np.array, agent_position: np.array) -> float:

        return np.any(position != agent_position) * \
               ((np.linalg.norm(position - agent_position) <= self.infection_radius) * self.viral_load)
