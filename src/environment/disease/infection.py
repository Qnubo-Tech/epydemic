from numpy.random import choice

from src.environment.disease.parameter import DiseaseParameter
from src.environment.status import Status
from src.configuration import (
    ImmunityParams,
    InfectionParams
)


class Infection(DiseaseParameter):

    def __init__(self,
                 mean_duration: float = InfectionParams.RECOVERY_TIME,
                 std_duration: float = InfectionParams.RECOVERY_TIME_ERR):

        super().__init__(mean_duration, std_duration)
        self.duration = self._set_duration()

    def _set_duration(self) -> float:
        if InfectionParams.RANDOM_RECOVERY_TIME:
            return self.random_value
        else:
            return self.default_value

    def check_recovery(self) -> Status:
        st = choice(
            [Status.Immune, Status.Healthy],
            p=[ImmunityParams.PROBABILITY, (1 - ImmunityParams.PROBABILITY)]
        )

        self.time = 0
        return st
