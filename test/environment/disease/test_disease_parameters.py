import pytest

from numpy import array

from src.environment.status import Status

from src.environment.disease.disease import Disease
from src.environment.disease.immunity import Immunity
from src.environment.disease.parameter import DiseaseParameter
from src.environment.disease.infection import Infection

from src.simulation.configuration import StochasticParams, Time, ImmunityParams


@pytest.fixture()
def disease_param():
    return DiseaseParameter(mean_duration=10, std_duration=1)


def test_default_duration(disease_param):
    assert disease_param.default_value == 10


def test_random_duration(disease_param):
    val_1, val_2 = disease_param.random_value, disease_param.random_value
    assert val_1 > 0
    assert val_2 > 0
    assert val_1 != val_2


def test_time(disease_param):
    assert disease_param.time == 0


def test_update_time(disease_param):
    disease_param.update_time()
    assert disease_param.time == Time.STEP_SEC


@pytest.fixture()
def immunity():
    StochasticParams.RANDOM_IMMUNITY = False
    return Immunity(mean_duration=10)


@pytest.fixture()
def random_immunity():
    StochasticParams.RANDOM_IMMUNITY = True
    return Immunity(mean_duration=10, std_duration=1)


def test_default_immunity(immunity):
    val_1, val_2 = immunity.duration, immunity.duration
    assert val_1 == val_2 == 10


def test_random_immunity(random_immunity):
    val_1, val_2 = random_immunity.duration, random_immunity.duration
    assert val_1 > 0
    assert val_2 > 0
    assert val_1 != val_2


def test_check_immunity_loss_time_below_duration(immunity):
    assert immunity.check_immunity_loss(status=Status.Immune) == Status.Immune


def test_check_immunity_loss_time_beyond_duration(immunity):
    default_value = ImmunityParams.LOSS_PROBABILITY

    ImmunityParams.LOSS_PROBABILITY = 1
    immunity.time = 20

    new_st = immunity.check_immunity_loss(status=Status.Immune)
    assert new_st == Status.Healthy
    assert immunity.time == 0

    ImmunityParams.LOSS_PROBABILITY = default_value


def test_check_immunity_loss_time_beyond_duration_no_change(immunity):
    default_value = ImmunityParams.LOSS_PROBABILITY

    ImmunityParams.LOSS_PROBABILITY = 0
    immunity.time = 20

    new_st = immunity.check_immunity_loss(status=Status.Immune)
    assert new_st == Status.Immune
    assert immunity.time == 20

    ImmunityParams.LOSS_PROBABILITY = default_value


@pytest.fixture(scope="module")
def infection():
    StochasticParams.RANDOM_RECOVERY = False
    return Infection(mean_duration=10)


@pytest.fixture(scope="module")
def random_infection():
    StochasticParams.RANDOM_RECOVERY = True
    return Infection(mean_duration=10, std_duration=1)


def test_default_infection(infection):
    val_1, val_2 = infection.duration, infection.duration
    assert val_1 == val_2 == 10


def test_random_infection(random_infection):
    val_1, val_2 = random_infection.duration, random_infection.duration
    assert val_1 > 0
    assert val_2 > 0
    assert val_1 != val_2


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


def test_force(disease):
    distant_agent_force = disease.force(position=array([0, 0]), agent_position=array([1, 1]))
    same_position_force = disease.force(position=array([0, 0]), agent_position=array([0, 0]))
    close_agent_force = disease.force(position=array([0, 0]), agent_position=array([0, 0.01]))

    assert distant_agent_force == 0
    assert same_position_force == 0
    assert close_agent_force == disease.viral_load
