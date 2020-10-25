import pytest

from numpy import array

from src.environment.status import Status

from src.environment.disease.disease import Disease
from src.environment.disease.immunity import Immunity
from src.environment.disease.parameter import DiseaseParameter
from src.environment.disease.recovery import Recovery

from src.simulation.configuration import StochasticParams, Time


@pytest.fixture(scope="module")
def disease_param():
    return DiseaseParameter(mean_duration=10, std_duration=1)


def test_default(disease_param):
    assert disease_param.default_value == 10


def test_random(disease_param):
    val_1, val_2 = disease_param.random_value, disease_param.random_value
    assert val_1 > 0
    assert val_2 > 0
    assert val_1 != val_2


@pytest.fixture(scope="module")
def immunity():
    StochasticParams.MEAN_IMMUNITY_SHIELD_TIME = False
    return Immunity(mean_duration=10)


@pytest.fixture(scope="module")
def random_immunity():
    StochasticParams.MEAN_IMMUNITY_SHIELD_TIME = True
    return Immunity(mean_duration=10, std_duration=1)


def test_default_duration(immunity):
    val_1, val_2 = immunity.duration, immunity.duration
    assert val_1 == val_2 == 10


def test_random_duration(random_immunity):
    val_1, val_2 = random_immunity.duration, random_immunity.duration
    assert val_1 > 0
    assert val_2 > 0
    assert val_1 != val_2


@pytest.fixture(scope="module")
def recovery():
    StochasticParams.MEAN_RECOVERY_TIME = False
    return Recovery(mean_duration=10)


@pytest.fixture(scope="module")
def random_recovery():
    StochasticParams.MEAN_RECOVERY_TIME = True
    return Recovery(mean_duration=10, std_duration=1)


def test_default_recovery(recovery):
    val_1, val_2 = recovery.duration, recovery.duration
    assert val_1 == val_2 == 10


def test_random_recovery(random_recovery):
    val_1, val_2 = random_recovery.duration, random_recovery.duration
    assert val_1 > 0
    assert val_2 > 0
    assert val_1 != val_2


@pytest.fixture
def disease() -> Disease:
    StochasticParams.MEAN_IMMUNITY_SHIELD_TIME = False
    StochasticParams.MEAN_RECOVERY_TIME = False
    ds = Disease(viral_load=1.0,
                 radius=0.02,
                 immunity=Immunity(mean_duration=10),
                 recovery=Recovery(mean_duration=7))
    return ds


def test_disease_initial_params(disease):
    assert disease.viral_load == 1.0
    assert disease.infection_radius == 0.02
    assert disease.mean_immunity_shield == 10
    assert disease.mean_recovery_time == 7
    assert disease.t_infected == 0
    assert disease.t_immunized == 0


def test_update_times_infected(disease):
    disease._update_times(status=Status.Infected)
    assert disease.t_infected == Time.STEP_SEC
    assert disease.t_immunized == 0


def test_update_times_healthy(disease):
    disease._update_times(status=Status.Healthy)
    assert disease.t_infected == 0
    assert disease.t_immunized == 0


def test_update_times_immune(disease):
    disease._update_times(status=Status.Immune)
    assert disease.t_infected == 0
    assert disease.t_immunized == Time.STEP_SEC


def test_update_times_confined(disease):
    disease._update_times(status=Status.Confined)
    assert disease.t_infected == Time.STEP_SEC
    assert disease.t_immunized == 0


def test_force(disease):
    distant_agent_force = disease.force(position=array([0, 0]), agent_position=array([1, 1]))
    same_position_force = disease.force(position=array([0, 0]), agent_position=array([0, 0]))
    close_agent_force = disease.force(position=array([0, 0]), agent_position=array([0, 0.01]))

    assert distant_agent_force == 0
    assert same_position_force == 0
    assert close_agent_force == disease.viral_load
