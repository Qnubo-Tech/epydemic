import logging
import matplotlib.pyplot as plt

from src.environment import Status, Society
from src.geometry.geometry import Geometry

from src.simulation import (
    Graph, Time, POPULATION, HEALTHY_PC, INFECTED_PC,
    RECOVERY_TIME_DAYS, IMMUNITY_SHIELD_TIME_DAYS,
    IMMUNITY_PROBABILITY, IMMUNITY_LOSS_PROBABILITY,
    CONFINED_PROBABILITY, VIRAL_STICKINESS
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def run():

    society = Society(
        population=POPULATION,
        initial_condition={"healthy": HEALTHY_PC, "infected": INFECTED_PC}
    )

    plt.ion()
    fig = plt.figure()
    gs = fig.add_gridspec(3, 4)
    ax1 = fig.add_subplot(gs[:, -2:])
    ax2 = fig.add_subplot(gs[1:, :-2])
    ax3 = fig.add_subplot(gs[0, :-2])

    times = []
    society_progress = {st.name: [] for st in Status}
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
        "Confined probability": CONFINED_PROBABILITY,
        "Viral stickiness": VIRAL_STICKINESS
    }

    Graph.plot_table_params(axis=ax3, params_dict=table_params)

    iteration = 0
    for dt in range(2000):
        society.make_step()

        if iteration == 0 or (iteration == 10):
            res = society.get_status()

            society_status = society.get_status()

            times.append(time / 3600 / 24)
            for st in Status:
                society_progress[st.name].append(society_status[st.name] / society_status["Total"])
                ax1.plot(times, society_progress[st.name], c=st.value, ls='-', label=st.name)

            ax1.set_ylim(0, Geometry.Box.Ly)

            society.plot(ax2)

            plt.show()
            logger.info(f"| {time / 3600}h - "
                        f"infected: {res[Status.Infected.name]}, "
                        f"healthy: {res[Status.Healthy.name]}, "
                        f"immune: {res[Status.Immune.name]}, "
                        f"confined: {res[Status.Confined.name]}")

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

