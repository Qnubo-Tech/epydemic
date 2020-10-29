from configparser import ConfigParser

config = ConfigParser()
config.read('src/simulation/config.ini')


class TimeConverter:
    MIN_TO_SEC = 60
    HOUR_TO_MIN = 60
    HOUR_TO_SEC = HOUR_TO_MIN * MIN_TO_SEC
    DAY_TO_HOUR = 24
    DAY_TO_MIN = DAY_TO_HOUR * HOUR_TO_MIN
    DAY_TO_SEC = DAY_TO_HOUR * HOUR_TO_SEC


class Time:
    STEP_SEC = config.getfloat('simulation', 'time_scale')
    STEP_MIN = STEP_SEC / TimeConverter.MIN_TO_SEC
    STEP_HOUR = STEP_MIN / TimeConverter.HOUR_TO_MIN


POPULATION = config.getfloat('simulation', 'population')
HEALTHY_PC = config.getfloat('simulation', 'healthy')
INFECTED_PC = config.getfloat('simulation', 'infected')

AVERAGE_MOBILITY = config.getfloat('agent.properties', 'mobility')
MOBILITY_TYPE = config.get('agent.properties', 'mobility_type').lower()
MOBILITY_HOURS_THRESHOLD = config.getint('agent.properties', 'mobility_hours')

INFECTION_RADIUS = config.getfloat('disease.properties', 'infection_radius')

RECOVERY_TIME_DAYS = config.getfloat('disease.properties', 'recovery_time_days')
RECOVERY_TIME = config.getfloat('disease.properties', 'recovery_time_days') * TimeConverter.DAY_TO_SEC
RECOVERY_TIME_ERR = config.getfloat('disease.properties', 'recovery_time_err_days') * TimeConverter.DAY_TO_SEC

CONFINED_PROBABILITY = config.getfloat('disease.properties', 'confined_probability')

VIRAL_LOAD_INFECTION_THRESHOLD = config.getfloat('disease.properties', 'viral_load_infection_threshold')
VIRAL_STICKINESS = config.getfloat('disease.properties', 'viral_stickiness')
VIRAL_UNLOADING_RATE = config.getfloat('disease.properties', 'viral_unloading_rate')

PLOT_PARAMETERS = config.getboolean('graph', 'plot_parameters')


class StochasticParams:
    MOBILITY_HOURS = False
    RANDOM_RECOVERY = False
    RANDOM_IMMUNITY = False
    AVERAGE_MOBILITY_INFECTION = False


class ImmunityParams:
    SHIELD_TIME_DAYS = config.getfloat('disease.immunity', 'immunity_shield_days')
    SHIELD_TIME = config.getfloat('disease.immunity',
                                  'immunity_shield_days') * TimeConverter.DAY_TO_SEC
    SHIELD_TIME_ERR = config.getfloat('disease.immunity',
                                      'immunity_shield_err_days') * TimeConverter.DAY_TO_SEC

    PROBABILITY = config.getfloat('disease.immunity', 'immunity_probability')
    LOSS_PROBABILITY = config.getfloat('disease.immunity', 'immunity_loss_probability')

