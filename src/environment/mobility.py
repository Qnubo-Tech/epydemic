from enum import Enum

import numpy as np

from src.simulation.configuration import MOBILITY_HOURS_THRESHOLD


class MobilityType(Enum):
    unlimited = "unlimited"
    hourly = "hourly"


class Mobility:

    def __init__(self, initial_value: float):
        self.value = initial_value

    def _random_step(self, mobility_args: dict):
        return np.random.normal(0, self.value * mobility_args["dt"], size=2)

    def update_position(self, mobility_args: dict):
        return


class UnlimitedMobility(Mobility):

    def __init__(self, initial_value: float):
        super().__init__(initial_value=initial_value)

    def update_position(self, mobility_args: dict):
        return self._random_step(mobility_args=mobility_args)


class HourlyMobility(Mobility):

    def __init__(self, initial_value: float):
        super().__init__(initial_value=initial_value)

    def update_position(self, mobility_args: dict):

        hour = (mobility_args["time_alive"] / mobility_args["dt"]) % 24
        if hour <= MOBILITY_HOURS_THRESHOLD:
            return self._random_step(mobility_args=mobility_args)
        else:
            return np.zeros(shape=2)


class MobilityFactory:
    Constructor = {
        MobilityType.unlimited: UnlimitedMobility,
        MobilityType.hourly: HourlyMobility
    }

    @staticmethod
    def build(mobility_type: MobilityType,  **kwargs):
        return MobilityFactory.Constructor[mobility_type](**kwargs)




