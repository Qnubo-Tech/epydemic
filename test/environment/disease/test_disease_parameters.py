import pytest

from src.environment.disease.immunity import Immunity
from src.environment.disease.parameter import DiseaseParameter
from src.environment.disease.recovery import Recovery

from src.simulation.configuration import StochasticParams


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
    return Immunity(mean_duration=10, std_duration=1)


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
    return Recovery(mean_duration=10, std_duration=1)


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
