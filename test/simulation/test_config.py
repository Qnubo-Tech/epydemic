from src.simulation.configuration import (
    Time, TimeConverter,
    ImmunityParams,
    POPULATION, HEALTHY_PC, INFECTED_PC,
    AVERAGE_MOBILITY, MOBILITY_TYPE, MOBILITY_HOURS_THRESHOLD,
    INFECTION_RADIUS,
    RECOVERY_TIME_DAYS, RECOVERY_TIME, RECOVERY_TIME_ERR,
    CONFINED_PROBABILITY,
    VIRAL_LOAD_INFECTION_THRESHOLD, VIRAL_STICKINESS, VIRAL_UNLOADING_RATE
)


def test_TimeConverter():
    assert TimeConverter.MIN_TO_SEC == 60
    assert TimeConverter.HOUR_TO_MIN == 60
    assert TimeConverter.HOUR_TO_SEC == 3600
    assert TimeConverter.DAY_TO_HOUR == 24
    assert TimeConverter.DAY_TO_MIN == 24 * 60
    assert TimeConverter.DAY_TO_SEC == 24 * 3600


def test_Time():
    assert Time.STEP_SEC == 3600
    assert Time.STEP_MIN == 60
    assert Time.STEP_HOUR == 1


def test_ImmunityParams():
    assert ImmunityParams.SHIELD_TIME_DAYS == 10
    assert ImmunityParams.SHIELD_TIME == 10 * 24 * 3600
    assert ImmunityParams.SHIELD_TIME_ERR == 5 * 24 * 3600
    assert ImmunityParams.PROBABILITY == 0.8
    assert ImmunityParams.LOSS_PROBABILITY == 0.5


def test_config_values():
    assert POPULATION == 54
    assert HEALTHY_PC == 0.99
    assert INFECTED_PC == 0.01
    assert AVERAGE_MOBILITY == 0.0001
    assert MOBILITY_TYPE == "unlimited"
    assert MOBILITY_HOURS_THRESHOLD == 17
    assert INFECTION_RADIUS == 0.02
    assert RECOVERY_TIME_DAYS == 7
    assert RECOVERY_TIME == 7 * 24 * 3600
    assert RECOVERY_TIME_ERR == 1 * 24 * 3600
    assert CONFINED_PROBABILITY == 0.01
    assert VIRAL_LOAD_INFECTION_THRESHOLD == 0.9
    assert VIRAL_STICKINESS == 0.3
    assert VIRAL_UNLOADING_RATE == 0.015
