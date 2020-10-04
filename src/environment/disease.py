from enum import Enum

import numpy as np

from src.simulation import Time, AVERAGE_MOBILITY


class Status(Enum):
    Infected = "red"
    Immune = "darkgreen"
    Healthy = "blue"


class Disease:

    MEAN_TIME_RECOVERY_IN_DAYS = 21
    MEAN_TIME_RECOVERY = MEAN_TIME_RECOVERY_IN_DAYS * 24 * 60 * 60
    TIME_RECOVERY_STDV_DAYS = 7
    TIME_RECOVERY_STDV = TIME_RECOVERY_STDV_DAYS * 24 * 60 * 60

    IMMUNITY_DEVELOPED_PROBABILITY = 0.4
    IMMUNITY_LOSING_PROBABILITY = 0.5

    SPREADING_PROBABILITY = 0.3

    MEAN_TIME_IMMUNITY_SHIELD_IN_DAYS = 30 * 3
    MEAN_TIME_IMMUNITY_SHIELD = MEAN_TIME_IMMUNITY_SHIELD_IN_DAYS * 24 * 60 * 60
    IMMUNITY_SHIELD_STDV_DAYS = 30 * 3
    IMMUNITY_SHIELD_STDV = IMMUNITY_SHIELD_STDV_DAYS * 24 * 60 * 60

    UNLOADING_RATE = 0.015

    def __init__(self, viral_load: float, radius: float):

        self.viral_load = viral_load
        self.infection_radius = radius
        # self.mean_recovery_time = max(0, np.random.normal(loc=Disease.MEAN_TIME_RECOVERY,
        #                                                   scale=Disease.TIME_RECOVERY_STDV))
        self.mean_recovery_time = 3 * 24 * 60 * 60
        # self.mean_immunity_shield = max(0, np.random.normal(loc=Disease.MEAN_TIME_IMMUNITY_SHIELD,
        #                                                     scale=Disease.IMMUNITY_SHIELD_STDV))
        self.mean_immunity_shield = 30 * 24 * 60 * 60
        self.t_infected = 0
        self.t_immunized = 0

    def _update_infection_times(self, status: Status):

        if status == Status.Infected:
            self.t_infected += Time.STEP_SEC
        if status == Status.Immune:
            self.t_immunized += Time.STEP_SEC

    def _update_viral_load(self, status, force):

        # Still infected:
        if (self.t_infected <= self.mean_recovery_time) and (status == Status.Infected):
            self.viral_load *= 1
            return status

        # Already passed the disease (but maybe not immune):
        if (self.t_infected > self.mean_recovery_time) and (status == Status.Infected):
            self.viral_load *= np.exp(-Disease.UNLOADING_RATE)

            n_status = np.random.choice(
                [Status.Immune, Status.Healthy],
                p=[Disease.IMMUNITY_DEVELOPED_PROBABILITY, (1-Disease.IMMUNITY_DEVELOPED_PROBABILITY)]
            )

            self.t_infected = 0
            return n_status

        # Healthy moving around
        if status == Status.Healthy:
            # Getting some infection:
            if force != 0:
                self.viral_load += min(Disease.SPREADING_PROBABILITY * force, 1.0)

            # Unloading because it left the dangerous region:
            else:
                self.viral_load *= np.exp(-Disease.UNLOADING_RATE)

            # Is is already infected?:
            if self.viral_load > 0.8:
                self.viral_load = 1
                return Status.Infected

            # It's still healthy:
            return status

        # For the immunes:
        else:
            self.viral_load *= np.exp(-Disease.UNLOADING_RATE)
            return status

    def _update_immune_agents(self, status):
        if (self.t_immunized > self.mean_immunity_shield) and (status == Status.Immune):
            st = np.random.choice([Status.Healthy, Status.Immune])
            if st == Status.Healthy:
                self.t_immunized = 0
            return status

    def _update_status(self, status):
        # self._update_immune_agents(status)
        return status

    @staticmethod
    def _get_sick_mobility():
        # return np.random.choice([1, 0], p=[0.8, 0.2])*AVERAGE_MOBILITY
        return AVERAGE_MOBILITY

    def _update_mobility(self, status):
        return (status == Status.Infected) * self._get_sick_mobility() \
               + (status != Status.Infected) * AVERAGE_MOBILITY

    def step(self, status: Status, force):

        self._update_infection_times(status=status)
        new_status = self._update_viral_load(status=status, force=force)
        new_status = self._update_status(status=new_status)
        new_mobility = self._update_mobility(status=new_status)
        return new_status, new_mobility

    def force(self, position: np.array, agent_position: np.array):

        return np.any(position != agent_position) * \
               ((np.linalg.norm(position - agent_position) <= self.infection_radius) * self.viral_load)