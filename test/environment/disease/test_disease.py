import pytest

from numpy import array, exp

from src.environment.status import Status

from src.environment.disease.disease import Disease
from src.environment.disease.immunity import Immunity
from src.environment.disease.infection import Infection

from src.simulation.configuration import (
    StochasticParams, Time, DiseaseParams
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
