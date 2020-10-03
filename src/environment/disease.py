from src.simulation import Time


class Disease:

    TIME_TO_RECOVERY_IN_DAYS = 2
    TAU = TIME_TO_RECOVERY_IN_DAYS * 24 * 60 * 60

    def __init__(self, viral_load: float, radius: float):

        self.viral_load = viral_load
        self.infection_radius = radius

        self.t_infected = 0

    def _update_infection_time(self):

        self.t_infected += Time.STEP_SEC

    def _update_viral_load(self):

        self.viral_load *= 1 if self.t_infected <= Disease.TAU else 0

    def step(self):

        self._update_infection_time()
        self._update_viral_load()
