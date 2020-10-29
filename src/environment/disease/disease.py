import numpy as np

from src.environment.status import Status

from src.simulation import (
    Time,
    StochasticParams,
    ImmunityParams,
    AVERAGE_MOBILITY,
    CONFINED_PROBABILITY,
    VIRAL_LOAD_INFECTION_THRESHOLD,
    VIRAL_STICKINESS,
    VIRAL_UNLOADING_RATE,
)

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

    def _update_viral_load(self, status, force):

        # Still infected:
        if (self.infection.time <= self.infection.duration) and (status == Status.Infected):
            self.viral_load *= 1

            # Check confined status
            n_status = np.random.choice(
                [Status.Confined, Status.Infected],
                p=[CONFINED_PROBABILITY, (1-CONFINED_PROBABILITY)]
            )

            return n_status

        # Already passed the disease (but maybe not immune):
        if (self.infection.time > self.infection.duration) and (status == Status.Infected):
            self.viral_load *= np.exp(-VIRAL_UNLOADING_RATE)

            n_status = np.random.choice(
                [Status.Immune, Status.Healthy],
                p=[ImmunityParams.PROBABILITY, (1 - ImmunityParams.PROBABILITY)]
            )

            #TODO: Assess the viral load when becoming Healthy
            # if (n_status == Status.Healthy):
            #     self.viral_load *= 0.5

            self.infection.time = 0
            return n_status

        # Healthy moving around
        if status == Status.Healthy:
            # Getting some infection:
            if force != 0:
                self.viral_load += VIRAL_STICKINESS * force
                self.viral_load = min(self.viral_load, 1.0)

            # Unloading because it left the dangerous region:
            else:
                self.viral_load *= np.exp(-VIRAL_UNLOADING_RATE)

            # Is is already infected?:
            if self.viral_load > VIRAL_LOAD_INFECTION_THRESHOLD:
                #self.viral_load = 1
                return Status.Infected

            # It's still healthy:
            return status

        # For the immunes and confined
        else:
            self.viral_load *= np.exp(-VIRAL_UNLOADING_RATE)
            return status

    def _update_status(self, status):
        if status == Status.Immune:
            return self.immunity.check_immunity_loss(status)
        elif status == Status.Confined:
            return self.infection.check_recovery(status)
        return status

    @staticmethod
    def _get_sick_mobility():
        if StochasticParams.AVERAGE_MOBILITY_INFECTION:
            return np.random.choice([1, 0], p=[0.8, 0.2])*AVERAGE_MOBILITY
        else:
            return AVERAGE_MOBILITY

    def _update_mobility(self, status):
        return (status == Status.Infected) * self._get_sick_mobility() \
               + (status == Status.Confined) * 0 \
               + (status != Status.Infected and status != Status.Confined) * AVERAGE_MOBILITY

    def step(self, status: Status, force):

        self._update_times(status=status)
        new_status = self._update_viral_load(status=status, force=force)
        new_status = self._update_status(status=new_status)
        new_mobility = self._update_mobility(status=new_status)
        return new_status, new_mobility

    def force(self, position: np.array, agent_position: np.array):

        return np.any(position != agent_position) * \
               ((np.linalg.norm(position - agent_position) <= self.infection_radius) * self.viral_load)
