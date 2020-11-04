from numpy.random import choice

from src.environment.disease.parameter import DiseaseParameter
from src.environment.status import Status
from src.configuration import ImmunityParams


class Immunity(DiseaseParameter):

    def __init__(self,
                 mean_duration: float = ImmunityParams.SHIELD_TIME,
                 std_duration: float = ImmunityParams.SHIELD_TIME_ERR):

        super().__init__(mean_duration, std_duration)

    @property
    def duration(self) -> float:
        if ImmunityParams.RANDOM_SHIELD_TIME:
            return self.random_value
        else:
            return self.default_value

    def check_immunity_loss(self) -> Status:
        st = choice(
            [Status.Healthy, Status.Immune],
            p=[ImmunityParams.LOSS_PROBABILITY, 1 - ImmunityParams.LOSS_PROBABILITY]
        )
        if st == Status.Healthy:
            self.time = 0
        return st
