import logging
import matplotlib.pyplot as plt

from src.environment import Status, Society
from src.geometry.geometry import Geometry

from src.simulation import (
    Graph, Time, POPULATION, HEALTHY_PC, INFECTED_PC,
    RECOVERY_TIME_DAYS, IMMUNITY_SHIELD_TIME_DAYS,
    IMMUNITY_PROBABILITY, IMMUNITY_LOSS_PROBABILITY,
    VIRAL_STICKINESS
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def run():

    society = Society(
        population=POPULATION,
        initial_condition={'healthy': HEALTHY_PC, 'infected': INFECTED_PC}
    )

    # plt.ion()
    # fig, ax = plt.subplots()
    # society.plot_field(ax=ax, mesh=Geometry.Box)
    # plt.show()
    #
    # fig, ax = plt.subplots()
    # society.plot(ax=ax)
    # plt.show()

    plt.ion()
    fig = plt.figure()
    gs = fig.add_gridspec(3, 4)
    ax1 = fig.add_subplot(gs[:, -2:])
    ax2 = fig.add_subplot(gs[1:, :-2])
    ax3 = fig.add_subplot(gs[0, :-2])

    immune, infected, healthy, confined, times = ([], [], [], [], [])
    time = 0

    ax1.set_xlabel('time / days')
    ax1.set_ylabel('N')

    table_params = {
        "Population": POPULATION,
        "Time scale [h]": Time.STEP_HOUR,
        "Mean recovery time [days]": RECOVERY_TIME_DAYS,
        "Mean immunity shield [days]": IMMUNITY_SHIELD_TIME_DAYS,
        "Immunity probability": IMMUNITY_PROBABILITY,
        "Loss immunity probability": IMMUNITY_LOSS_PROBABILITY,
        "Viral stickiness": VIRAL_STICKINESS
    }

    Graph.plot_table_params(axis=ax3, params_dict=table_params)

    iteration = 0
    for dt in range(2000):
        society.make_step()

        if iteration == 0 or (iteration == 10):
            res = society.get_status()
            immune.append(res['immune'] / res['total'])
            healthy.append(res['healthy'] / res['total'])
            infected.append(res['infected'] / res['total'])
            confined.append(res['confined'] / res['total'])
            times.append(time / 3600 / 24)

            ax1.plot(times, healthy, c=Status.Healthy.value, ls='--', label=Status.Healthy.name)
            ax1.plot(times, infected, c=Status.Infected.value, marker="o", ls='-', label=Status.Infected.name)
            ax1.plot(times, immune, c=Status.Immune.value, ls=':', label=Status.Immune.name)
            ax1.plot(times, confined, c=Status.Confined.value, marker='*', ls='-', label=Status.Confined.name)

            ax1.set_ylim(0, Geometry.Box.Ly)

            society.plot(ax2)

            plt.show()
            logger.info(f'| {time / 3600}h - infected: {res["infected"]}, healthy: {res["healthy"]}, immune: {res["immune"]}, confined: {res["confined"]}')

        if iteration == 0:
            ax1.legend(loc=2)

        if iteration == 0 or (iteration == 10):
            iteration = 1
            plt.pause(0.01)

        time += Time.STEP_SEC
        iteration += 1

    plt.show()
    plt.pause(60)


if __name__ == "__main__":

    run()

