from numpy.random import choice

from src.environment.disease.parameter import DiseaseParameter
from src.environment.status import Status
from src.simulation import (
    StochasticParams,
    ImmunityParams,
    InfectionParams
)


class Infection(DiseaseParameter):

    def __init__(self,
                 mean_duration: float = InfectionParams.RECOVERY_TIME,
                 std_duration: float = InfectionParams.RECOVERY_TIME_ERR):

        super().__init__(mean_duration, std_duration)

    @property
    def duration(self) -> float:
        if StochasticParams.RANDOM_RECOVERY:
            return self.random_value
        else:
            return self.default_value

    def check_confinement(self) -> Status:
        st = choice(
            [Status.Confined, Status.Infected],
            p=[InfectionParams.CONFINED_PROBABILITY, (1 - InfectionParams.CONFINED_PROBABILITY)]
        )

        return st

    def check_recovery(self) -> Status:
        st = choice(
            [Status.Immune, Status.Healthy],
            p=[ImmunityParams.PROBABILITY, (1 - ImmunityParams.PROBABILITY)]
        )

        self.time = 0
        return st
