from src.environment.disease.parameter import DiseaseParameter
from src.simulation import (
    StochasticParams, RECOVERY_TIME, RECOVERY_TIME_ERR
)


class Recovery(DiseaseParameter):

    def __init__(self,
                 mean_duration: float = RECOVERY_TIME,
                 std_duration: float = RECOVERY_TIME_ERR):

        super().__init__(mean_duration, std_duration)

    @property
    def duration(self):
        if StochasticParams.MEAN_RECOVERY_TIME:
            return self.random_value
        else:
            return self.default_value
