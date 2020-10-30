import pytest

from src.simulation.configuration import Time, MobilityParams

from src.environment.mobility import (
    Mobility,
    MobilityType,
    UnlimitedMobility,
    CurfewMobility
)
from src.environment.status import Status


@pytest.fixture()
def mobility_type_dict():
    mobility_dict = {
        "unlimited": "unlimited",
        "curfew": "curfew"
    }
    return mobility_dict


def test_names(mobility_type_dict):
    for st in mobility_type_dict.keys():
        assert st in MobilityType.__members__


def test_values(mobility_type_dict):
    for k, v in mobility_type_dict.items():
        assert v == MobilityType[k].value


@pytest.fixture()
def mobility() -> Mobility:
    return Mobility(initial_value=0.0001)


def test_initial_values(mobility):
    assert mobility.default_value == 0.0001
    assert mobility.value == 0.0001


def test_infected_mobility_with_zero_prob(mobility):
    default_value = MobilityParams.RESTRICTION_PROBABILITY
    MobilityParams.RESTRICTION_PROBABILITY = 0

    assert mobility.infected_mobility == mobility.default_value
    MobilityParams.RESTRICTION_PROBABILITY = default_value


def test_infected_mobility_with_one_prob(mobility):
    default_value = MobilityParams.RESTRICTION_PROBABILITY
    MobilityParams.RESTRICTION_PROBABILITY = 1

    assert mobility.infected_mobility == 0
    MobilityParams.RESTRICTION_PROBABILITY = default_value


def test_confined_mobility(mobility):
    assert mobility.confined_mobility == 0


def test_random_step(mobility):
    step = mobility._random_step()
    assert step.size == 2
    assert step[0] != step[1]


def test_update_value_infected(mobility):
    default_value = MobilityParams.RESTRICTION_PROBABILITY
    MobilityParams.RESTRICTION_PROBABILITY = 1

    mobility.update_value(status=Status.Infected)
    assert mobility.value == 0

    MobilityParams.RESTRICTION_PROBABILITY = default_value


def test_update_value_confined(mobility):
    mobility.update_value(status=Status.Confined)
    assert mobility.value == mobility.confined_mobility


def test_update_value_healthy(mobility):
    mobility.update_value(status=Status.Healthy)
    assert mobility.value == mobility.default_value


def test_update_value_immune(mobility):
    mobility.update_value(status=Status.Immune)
    assert mobility.value == mobility.default_value


@pytest.fixture()
def unlimited_mobility() -> UnlimitedMobility:
    return UnlimitedMobility(initial_value=0.0001)


def test_update_position(unlimited_mobility):
    step = unlimited_mobility.update_position(mobility_args={})
    assert step.size == 2
    assert step[0] != step[1]


@pytest.fixture()
def curfew_mobility() -> CurfewMobility:
    return CurfewMobility(initial_value=0.0001)


def test_update_position_before_curfew(curfew_mobility):
    mobility_args = {
        "time_alive": 0
    }

    default_value = MobilityParams.CURFEW_THRESHOLD
    MobilityParams.CURFEW_THRESHOLD = 20

    step = curfew_mobility.update_position(mobility_args=mobility_args)

    assert step.size == 2
    assert step[0] != step[1]

    MobilityParams.CURFEW_THRESHOLD = default_value


def test_update_position_after_curfew(curfew_mobility):
    mobility_args = {
        "time_alive": 21 * Time.STEP_SEC
    }

    default_value = MobilityParams.CURFEW_THRESHOLD
    MobilityParams.CURFEW_THRESHOLD = 20

    step = curfew_mobility.update_position(mobility_args=mobility_args)

    assert step.size == 2
    assert step[0] == 0
    assert step[1] == 0

    MobilityParams.CURFEW_THRESHOLD = default_value
