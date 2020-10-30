from enum import Enum

import numpy as np

from src.environment.status import Status

from src.simulation.configuration import (
    Time, TimeConverter,
    MobilityParams
)


class MobilityType(Enum):
    unlimited = "unlimited"
    curfew = "curfew"


class Mobility:

    def __init__(self, initial_value: float):
        self.default_value = initial_value
        self.value = initial_value

    @property
    def infected_mobility(self):
        return np.random.choice(
            [0, self.default_value],
            p=[MobilityParams.RESTRICTION_PROBABILITY, 1-MobilityParams.RESTRICTION_PROBABILITY]
        )

    @property
    def confined_mobility(self):
        return 0

    def _random_step(self):
        return np.random.normal(0, self.value * Time.STEP_SEC, size=2)

    def update_position(self, mobility_args: dict):
        return

    def update_value(self, status: Status):
        if status == Status.Infected:
            self.value = self.infected_mobility
        elif status == Status.Confined:
            self.value = self.confined_mobility
        else:
            self.value = self.default_value


class UnlimitedMobility(Mobility):

    def __init__(self, initial_value: float):
        super().__init__(initial_value=initial_value)

    def update_position(self, mobility_args: dict):
        return self._random_step()


class CurfewMobility(Mobility):

    def __init__(self, initial_value: float):
        super().__init__(initial_value=initial_value)

    def update_position(self, mobility_args: dict):

        hour = (mobility_args["time_alive"] / Time.STEP_SEC) % TimeConverter.DAY_TO_HOUR
        if hour <= MobilityParams.CURFEW_THRESHOLD:
            return self._random_step()
        else:
            return np.zeros(shape=2)


class MobilityFactory:
    Constructor = {
        MobilityType.unlimited: UnlimitedMobility,
        MobilityType.curfew: CurfewMobility
    }

    @staticmethod
    def build(mobility_type: MobilityType,  **kwargs):
        return MobilityFactory.Constructor[mobility_type](**kwargs)
