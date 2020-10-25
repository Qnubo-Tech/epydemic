from numpy.random import normal


class DiseaseParameter:

    def __init__(self, mean_duration: float, std_duration: float):

        self.mean = mean_duration
        self.std = std_duration

    @property
    def default_value(self):
        return self.mean

    @property
    def random_value(self):
        return max(0, normal(loc=self.mean, scale=self.std))
