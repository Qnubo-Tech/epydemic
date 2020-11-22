from configparser import ConfigParser

config = ConfigParser()
config.read('src/configuration/config.ini')


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


PLOT_PARAMETERS = config.getboolean('graph', 'plot_parameters')


class SocietyParams:
    POPULATION = config.getfloat('society.parameters', 'population')
    HEALTHY_PC = config.getfloat('society.parameters', 'healthy')
    INFECTED_PC = config.getfloat('society.parameters', 'infected')


class ConfinementParams:
    CONFINEMENT_CAPACITY = config.getfloat('society.confinement', 'capacity')
    ELIGIBLE_POPULATION_SHARE = config.getfloat('society.confinement', 'eligible_population_share')


class DiseaseParams:
    INFECTION_RADIUS = config.getfloat('disease.parameters', 'infection_radius')

    VIRAL_LOAD_INFECTION_THRESHOLD = config.getfloat('disease.parameters',
                                                     'viral_load_infection_threshold')
    VIRAL_STICKINESS = config.getfloat('disease.parameters', 'viral_stickiness')
    VIRAL_UNLOADING_RATE = config.getfloat('disease.parameters', 'viral_unloading_rate')


class ImmunityParams:
    SHIELD_TIME_DAYS = config.getfloat('disease.immunity', 'immunity_shield_days')
    SHIELD_TIME = config.getfloat('disease.immunity',
                                  'immunity_shield_days') * TimeConverter.DAY_TO_SEC
    SHIELD_TIME_ERR = config.getfloat('disease.immunity',
                                      'immunity_shield_err_days') * TimeConverter.DAY_TO_SEC

    RANDOM_SHIELD_TIME = config.getboolean('disease.immunity', 'random_shield_time')

    PROBABILITY = config.getfloat('disease.immunity', 'immunity_probability')
    LOSS_PROBABILITY = config.getfloat('disease.immunity', 'immunity_loss_probability')


class InfectionParams:
    RECOVERY_TIME_DAYS = config.getfloat('disease.infection', 'recovery_time_days')
    RECOVERY_TIME = config.getfloat('disease.infection',
                                    'recovery_time_days') * TimeConverter.DAY_TO_SEC
    RECOVERY_TIME_ERR = config.getfloat('disease.infection',
                                        'recovery_time_err_days') * TimeConverter.DAY_TO_SEC

    RANDOM_RECOVERY_TIME = config.getboolean('disease.infection', 'random_recovery_time')


class MobilityParams:
    DEFAULT_MOBILITY = config.getfloat('agent.mobility', 'mobility')
    RESTRICTION_PROBABILITY = config.getfloat('agent.mobility', 'restricted_probability')
    MOBILITY_TYPE = config.get('agent.mobility', 'mobility_type').lower()
    CURFEW_THRESHOLD = config.getint('agent.mobility', 'curfew_threshold')
