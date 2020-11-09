from typing import NoReturn

from numpy.random import normal

from src.configuration import Time


class DiseaseParameter:

    def __init__(self, mean_duration: float, std_duration: float):

        self.mean = mean_duration
        self.std = std_duration
        self.time = 0

        self.default_value = mean_duration
        self.random_value = max(0, normal(loc=self.mean, scale=self.std))

    def update_time(self) -> NoReturn:
        self.time += Time.STEP_SEC
