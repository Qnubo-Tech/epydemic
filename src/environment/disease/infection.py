from numpy.random import choice

from src.environment.disease.parameter import DiseaseParameter
from src.environment.status import Status
from src.simulation import (
    StochasticParams,
    ImmunityParams,
    RECOVERY_TIME, RECOVERY_TIME_ERR
)


class Infection(DiseaseParameter):

    def __init__(self,
                 mean_duration: float = RECOVERY_TIME,
                 std_duration: float = RECOVERY_TIME_ERR):

        super().__init__(mean_duration, std_duration)

    @property
    def duration(self) -> float:
        if StochasticParams.RANDOM_RECOVERY:
            return self.random_value
        else:
            return self.default_value

    def check_recovery(self, status) -> Status:
        if self.time > self.duration:
            st = choice(
                [Status.Immune, Status.Healthy],
                p=[ImmunityParams.PROBABILITY, (1 - ImmunityParams.PROBABILITY)]
            )

            self.time = 0
            return st

        return status
