from configparser import ConfigParser

config = ConfigParser()
config.read('simulation/config.ini')


AVERAGE_MOBILITY = config.getfloat('agent.properties', 'mobility')
MOBILITTY_HOURS_THRESHOLD = config.getint('agent.properties', 'mobility_hours')

POPULATION = config.getfloat('simulation', 'population')
HEALTHY_PC = config.getfloat('simulation', 'healthy')
INFECTED_PC = config.getfloat('simulation', 'infected')

RECOVERY_TIME_DAYS = config.getfloat('disease.properties', 'recovery_time_days')
RECOVERY_TIME = config.getfloat('disease.properties', 'recovery_time_days') * 24 * 3600
RECOVERY_TIME_ERR = config.getfloat('disease.properties', 'recovery_time_err_days') * 24 * 3600

IMMUNITY_PROBABILITY = config.getfloat('disease.properties', 'immunity_probability')
IMMUNITY_LOSS_PROBABILITY = config.getfloat('disease.properties', 'immunity_loss_probability')

CONFINED_PROBABILITY = config.getfloat('disease.properties', 'confined_probability')

VIRAL_STICKINESS = config.getfloat('disease.properties', 'viral_stickiness')
VIRAL_UNLOADING_RATE = config.getfloat('disease.properties', 'viral_unloading_rate')

IMMUNITY_SHIELD_TIME_DAYS = config.getfloat('disease.properties', 'immunity_shield_days')
IMMUNITY_SHIELD_TIME = config.getfloat('disease.properties', 'immunity_shield_days') * 24 * 3600
IMMUNITY_SHIELD_TIME_ERR = config.getfloat('disease.properties', 'immunity_shield_err_days') * 24 * 3600


class Time:
    STEP_SEC = config.getfloat('simulation', 'time_scale')
    STEP_MIN = STEP_SEC / 60
    STEP_HOUR = STEP_MIN / 60


class StochasticParams:
    MOBILITY_HOURS = False
    MEAN_RECOVERY_TIME = False
    MEAN_IMMUNITY_SHIELD_TIME = False
    AVERAGE_MOBILITY_INFECTION = False
