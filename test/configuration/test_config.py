from src.configuration.configuration import (
    Time, TimeConverter,
    SocietyParams,
    DiseaseParams,
    ImmunityParams,
    InfectionParams,
    MobilityParams
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


def test_SocietyParams():
    assert SocietyParams.POPULATION == 54
    assert SocietyParams.HEALTHY_PC == 0.99
    assert SocietyParams.INFECTED_PC == 0.01


def test_DiseaseParams():
    assert DiseaseParams.INFECTION_RADIUS == 0.02
    assert DiseaseParams.VIRAL_LOAD_INFECTION_THRESHOLD == 0.9
    assert DiseaseParams.VIRAL_STICKINESS == 0.3
    assert DiseaseParams.VIRAL_UNLOADING_RATE == 0.015


def test_ImmunityParams():
    assert ImmunityParams.SHIELD_TIME_DAYS == 10
    assert ImmunityParams.SHIELD_TIME == 10 * 24 * 3600
    assert ImmunityParams.SHIELD_TIME_ERR == 5 * 24 * 3600
    assert ImmunityParams.PROBABILITY == 0.8
    assert ImmunityParams.LOSS_PROBABILITY == 0.5


def test_InfectionParams():
    assert InfectionParams.RECOVERY_TIME_DAYS == 7
    assert InfectionParams.RECOVERY_TIME == 7 * 24 * 3600
    assert InfectionParams.RECOVERY_TIME_ERR == 1 * 24 * 3600
    assert InfectionParams.CONFINED_PROBABILITY == 0.01


def test_MobilityParams():
    assert MobilityParams.DEFAULT_MOBILITY == 0.0001
    assert MobilityParams.RESTRICTION_PROBABILITY == 0
    assert MobilityParams.MOBILITY_TYPE == "unlimited"
    assert MobilityParams.CURFEW_THRESHOLD == 17

