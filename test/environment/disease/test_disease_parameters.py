import pytest

from src.environment.status import Status

from src.environment.disease.immunity import Immunity
from src.environment.disease.parameter import DiseaseParameter
from src.environment.disease.infection import Infection

from src.simulation.configuration import StochasticParams, Time, ImmunityParams, InfectionParams


@pytest.fixture()
def disease_param() -> DiseaseParameter:
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
def immunity() -> Immunity:
    StochasticParams.RANDOM_IMMUNITY = False
    return Immunity(mean_duration=10)


@pytest.fixture()
def random_immunity() -> Immunity:
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


def test_check_immunity_loss_zero_prob(immunity):
    default_value = ImmunityParams.LOSS_PROBABILITY

    ImmunityParams.LOSS_PROBABILITY = 0
    immunity.time = 20

    assert immunity.check_immunity_loss() == Status.Immune
    assert immunity.time == 20

    ImmunityParams.LOSS_PROBABILITY = default_value


def test_check_immunity_loss_one_prob(immunity):
    default_value = ImmunityParams.LOSS_PROBABILITY

    ImmunityParams.LOSS_PROBABILITY = 1
    immunity.time = 20

    assert immunity.check_immunity_loss() == Status.Healthy
    assert immunity.time == 0

    ImmunityParams.LOSS_PROBABILITY = default_value


@pytest.fixture()
def infection() -> Infection:
    StochasticParams.RANDOM_RECOVERY = False
    return Infection(mean_duration=10)


@pytest.fixture()
def random_infection() -> Infection:
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


def test_check_recovery_to_immunity(infection):
    default_value = ImmunityParams.PROBABILITY

    ImmunityParams.PROBABILITY = 1
    infection.time = 20

    assert infection.check_recovery() == Status.Immune
    assert infection.time == 0

    ImmunityParams.PROBABILITY = default_value


def test_check_recovery_to_healthy(infection):
    default_value = ImmunityParams.PROBABILITY

    ImmunityParams.PROBABILITY = 0
    infection.time = 20

    assert infection.check_recovery() == Status.Healthy
    assert infection.time == 0

    ImmunityParams.PROBABILITY = default_value


def test_check_confinement_zero_prob(infection):
    default_value = InfectionParams.CONFINED_PROBABILITY

    InfectionParams.CONFINED_PROBABILITY = 0

    assert infection.check_confinement() == Status.Infected

    InfectionParams.CONFINED_PROBABILITY = default_value


def test_check_confinement_one_prob(infection):
    default_value = InfectionParams.CONFINED_PROBABILITY

    InfectionParams.CONFINED_PROBABILITY = 1

    assert infection.check_confinement() == Status.Confined

    InfectionParams.CONFINED_PROBABILITY = default_value
