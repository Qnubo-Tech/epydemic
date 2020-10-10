from enum import Enum

import numpy as np

from src.simulation import (
    Time,
    AVERAGE_MOBILITY,
    RECOVERY_TIME,
    RECOVERY_TIME_ERR,
    IMMUNITY_SHIELD_TIME,
    IMMUNITY_SHIELD_TIME_ERR,
    IMMUNITY_PROBABILITY,
    IMMUNITY_LOSS_PROBABILITY,
    CONFINED_PROBABILITY,
    VIRAL_STICKINESS,
    VIRAL_UNLOADING_RATE,
)


class Status(Enum):
    Infected = "red"
    Immune = "darkgreen"
    Healthy = "blue"
    Confined = "orange"


class Disease:

    def __init__(self, viral_load: float, radius: float):

        self.viral_load = viral_load
        self.infection_radius = radius

        self.mean_recovery_time = max(0, np.random.normal(loc=RECOVERY_TIME,
                                                          scale=RECOVERY_TIME_ERR))
        #self.mean_recovery_time = RECOVERY_TIME

        self.mean_immunity_shield = max(0, np.random.normal(loc=IMMUNITY_SHIELD_TIME,
                                                            scale=IMMUNITY_SHIELD_TIME_ERR))
        #self.mean_immunity_shield = IMMUNITY_SHIELD_TIME

        self.t_infected, self.t_immunized = (0, 0)

    def _update_infection_times(self, status: Status):

        if (status == Status.Infected) or (status == Status.Confined):
            self.t_infected += Time.STEP_SEC
        if status == Status.Immune:
            self.t_immunized += Time.STEP_SEC

    def _update_viral_load(self, status, force):

        # Still infected:
        if (self.t_infected <= self.mean_recovery_time) and (status == Status.Infected):
            self.viral_load *= 1

            # Check confined status
            n_status = np.random.choice(
                [Status.Confined, Status.Infected],
                p=[CONFINED_PROBABILITY, (1-CONFINED_PROBABILITY)]
            )

            return n_status

        # Already passed the disease (but maybe not immune):
        if (self.t_infected > self.mean_recovery_time) and (status == Status.Infected):
            self.viral_load *= np.exp(-VIRAL_UNLOADING_RATE)

            n_status = np.random.choice(
                [Status.Immune, Status.Healthy],
                p=[IMMUNITY_PROBABILITY, (1-IMMUNITY_PROBABILITY)]
            )

            self.t_infected = 0
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
            if self.viral_load > 0.9:
                #self.viral_load = 1
                return Status.Infected

            # It's still healthy:
            return status

        # For the immunes and confined
        else:
            self.viral_load *= np.exp(-VIRAL_UNLOADING_RATE)
            return status

    def _update_immune_agents(self, status):
        if self.t_immunized > self.mean_immunity_shield:
            st = np.random.choice(
                [Status.Healthy, Status.Immune],
                p=[IMMUNITY_LOSS_PROBABILITY, 1-IMMUNITY_LOSS_PROBABILITY]
            )
            if st == Status.Healthy:
                self.t_immunized = 0
            return st

        return status

    def _update_confined_agents(self, status):
        if self.t_infected > self.mean_recovery_time:
            st = np.random.choice(
                [Status.Immune, Status.Healthy],
                p=[IMMUNITY_PROBABILITY, (1-IMMUNITY_PROBABILITY)]
            )

            self.t_infected = 0
            return st

        return status

    def _update_status(self, status):
        if status == Status.Immune:
            return self._update_immune_agents(status)
        elif status == Status.Confined:
            return self._update_confined_agents(status)
        return status
        #return status

    @staticmethod
    def _get_sick_mobility():
        return np.random.choice([1, 0], p=[0.8, 0.2])*AVERAGE_MOBILITY
        #return AVERAGE_MOBILITY

    def _update_mobility(self, status):
        return (status == Status.Infected) * self._get_sick_mobility() \
               + (status == Status.Confined) * 0 \
               + (status != Status.Infected and status != Status.Confined) * AVERAGE_MOBILITY

    def step(self, status: Status, force):

        self._update_infection_times(status=status)
        new_status = self._update_viral_load(status=status, force=force)
        new_status = self._update_status(status=new_status)
        new_mobility = self._update_mobility(status=new_status)
        return new_status, new_mobility

    def force(self, position: np.array, agent_position: np.array):

        return np.any(position != agent_position) * \
               ((np.linalg.norm(position - agent_position) <= self.infection_radius) * self.viral_load)