from src.environment.disease.parameter import DiseaseParameter
from src.simulation import (
    StochasticParams, IMMUNITY_SHIELD_TIME, IMMUNITY_SHIELD_TIME_ERR
)


class Immunity(DiseaseParameter):

    def __init__(self,
                 mean_duration: float = IMMUNITY_SHIELD_TIME,
                 std_duration: float = IMMUNITY_SHIELD_TIME_ERR):

        super().__init__(mean_duration, std_duration)

    @property
    def duration(self):
        if StochasticParams.MEAN_IMMUNITY_SHIELD_TIME:
            return self.random_value
        else:
            return self.default_value
