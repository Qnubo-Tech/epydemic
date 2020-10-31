import pytest

from numpy import array, exp

from src.environment.status import Status

from src.environment.disease.disease import Disease
from src.environment.disease.immunity import Immunity
from src.environment.disease.infection import Infection

from src.configuration.configuration import (
    StochasticParams, Time,
    DiseaseParams,
    ImmunityParams,
    InfectionParams
)


@pytest.fixture
def disease() -> Disease:
    StochasticParams.RANDOM_IMMUNITY = False
    StochasticParams.RANDOM_RECOVERY = False
    ds = Disease(viral_load=1.0,
                 radius=0.02,
                 immunity=Immunity(mean_duration=10),
                 infection=Infection(mean_duration=7))
    return ds


def test_disease_initial_params(disease):
    assert disease.viral_load == 1.0
    assert disease.infection_radius == 0.02
    assert disease.immunity.duration == 10
    assert disease.immunity.time == 0
    assert disease.infection.duration == 7
    assert disease.infection.time == 0


def test_update_times_infected(disease):
    disease._update_times(status=Status.Infected)
    assert disease.infection.time == Time.STEP_SEC
    assert disease.immunity.time == 0


def test_update_times_healthy(disease):
    disease._update_times(status=Status.Healthy)
    assert disease.infection.time == 0
    assert disease.immunity.time == 0


def test_update_times_immune(disease):
    disease._update_times(status=Status.Immune)
    assert disease.infection.time == 0
    assert disease.immunity.time == Time.STEP_SEC


def test_update_times_confined(disease):
    disease._update_times(status=Status.Confined)
    assert disease.infection.time == Time.STEP_SEC
    assert disease.immunity.time == 0


def test_keep_viral_load(disease):
    disease.viral_load = 0.8
    disease._keep_viral_load()
    assert disease.viral_load == 0.8


def test_unload_viral_load(disease):
    disease.viral_load = 0.5
    disease._unload_viral_load()
    assert disease.viral_load == (0.5 * exp(-DiseaseParams.VIRAL_UNLOADING_RATE))


def test_increase_viral_load(disease):
    disease.viral_load = 0.5
    force = 0.1
    disease._increase_viral_load(force=force)
    assert disease.viral_load == (0.5 + DiseaseParams.VIRAL_STICKINESS * force)


def test_increase_viral_load_limit(disease):
    disease.viral = 1.3
    force = 1
    disease._increase_viral_load(force=force)
    assert disease.viral_load == 1


def test_force(disease):
    distant_agent_force = disease.force(position=array([0, 0]), agent_position=array([1, 1]))
    same_position_force = disease.force(position=array([0, 0]), agent_position=array([0, 0]))
    close_agent_force = disease.force(position=array([0, 0]), agent_position=array([0, 0.01]))

    assert distant_agent_force == 0
    assert same_position_force == 0
    assert close_agent_force == disease.viral_load


def test_dynamics_keep_infected(disease):
    disease.viral_load = 1
    disease.infection.time = 1

    default_value = InfectionParams.CONFINED_PROBABILITY
    InfectionParams.CONFINED_PROBABILITY = 0

    assert disease._update_dynamics(status=Status.Infected, force=1) == Status.Infected
    assert disease.viral_load == 1
    assert disease.infection.time == 1

    InfectionParams.CONFINED_PROBABILITY = default_value


def test_dynammics_infected_to_confined(disease):
    disease.viral_load = 1
    disease.infection.time = 1

    default_value = InfectionParams.CONFINED_PROBABILITY
    InfectionParams.CONFINED_PROBABILITY = 1

    assert disease._update_dynamics(status=Status.Infected, force=1) == Status.Confined
    assert disease.viral_load == 1
    assert disease.infection.time == 1

    InfectionParams.CONFINED_PROBABILITY = default_value


def test_dynammics_infected_to_immune(disease):
    disease.viral_load = 1
    disease.infection.time = 10

    default_value = ImmunityParams.PROBABILITY
    ImmunityParams.PROBABILITY = 1

    assert disease._update_dynamics(status=Status.Infected, force=1) == Status.Immune
    assert disease.viral_load == (1 * exp(-DiseaseParams.VIRAL_UNLOADING_RATE))
    assert disease.infection.time == 0

    ImmunityParams.PROBABILITY = default_value


def test_dynamics_healthy_no_force(disease):
    disease.viral_load = 0.1
    force = 0

    assert disease._update_dynamics(status=Status.Healthy, force=force) == Status.Healthy
    assert disease.viral_load == (0.1 * exp(-DiseaseParams.VIRAL_UNLOADING_RATE))


def test_dynamics_healthy_force(disease):
    disease.viral_load = 0.1
    force = 0.5

    assert disease._update_dynamics(status=Status.Healthy, force=force) == Status.Healthy
    assert disease.viral_load == (0.1 + DiseaseParams.VIRAL_STICKINESS * force)


def test_dynamics_healthy_to_infected(disease):
    disease.viral_load = 0.8
    force = 1

    assert disease._update_dynamics(status=Status.Healthy, force=force) == Status.Infected
    assert disease.viral_load == 1


def test_dynamics_immune_to_immune(disease):
    disease.viral_load = 0.5
    disease.immunity.time = 0

    assert disease._update_dynamics(status=Status.Immune, force=0) == Status.Immune
    assert disease.viral_load == (0.5 * exp(-DiseaseParams.VIRAL_UNLOADING_RATE))


def test_dynamics_immune_to_healthy(disease):
    disease.viral_load = 0.5
    disease.immunity.time = 20

    default_value = ImmunityParams.LOSS_PROBABILITY
    ImmunityParams.LOSS_PROBABILITY = 1

    assert disease._update_dynamics(status=Status.Immune, force=0) == Status.Healthy
    assert disease.immunity.time == 0
    assert disease.viral_load == (0.5 * exp(-DiseaseParams.VIRAL_UNLOADING_RATE))

    ImmunityParams.LOSS_PROBABILITY = default_value


def test_dynamic_confined_to_confined(disease):
    disease.viral_load = 0.5
    disease.infection.time = 0

    assert disease._update_dynamics(status=Status.Confined, force=0) == Status.Confined
    assert disease.viral_load == (0.5 * exp(-DiseaseParams.VIRAL_UNLOADING_RATE))


def test_dynamic_confined_to_healthy(disease):
    disease.viral_load = 0.5
    disease.infection.time = 10

    default_value = ImmunityParams.PROBABILITY
    ImmunityParams.PROBABILITY = 0

    assert disease._update_dynamics(status=Status.Confined, force=0) == Status.Healthy
    assert disease.viral_load == (0.5 * exp(-DiseaseParams.VIRAL_UNLOADING_RATE))
    assert disease.infection.time == 0

    ImmunityParams.PROBABILITY = default_value
