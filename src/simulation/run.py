import logging
import matplotlib.pyplot as plt
import numpy as np

from src.environment.society import Society
from src.environment.disease import Status
from src.geometry.geometry import Geometry

from src.simulation import (
    Graph, Time, POPULATION, HEALTHY_PC, INFECTED_PC,
    RECOVERY_TIME_DAYS, IMMUNITY_SHIELD_TIME_DAYS,
    IMMUNITY_PROBABILITY, IMMUNITY_LOSS_PROBABILITY,
    CONFINED_PROBABILITY, VIRAL_STICKINESS,
    PLOT_PARAMETERS
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

np.random.seed(0)


def run():

    society = Society(
        population=POPULATION,
        initial_condition={"healthy": HEALTHY_PC, "infected": INFECTED_PC}
    )

    plt.ion()

    fig, axis = Graph.generate_fig_ax(show_params=PLOT_PARAMETERS)

    # fig = plt.figure()
    # gs = fig.add_gridspec(3, 4)
    # ax1 = fig.add_subplot(gs[:, -2:])
    # ax2 = fig.add_subplot(gs[1:, :-2])
    # ax3 = fig.add_subplot(gs[0, :-2])

    times = []
    society_progress = {st.name: [] for st in Status}
    time = 0

    axis[0].set_xlabel('time [days]')
    axis[0].set_ylabel('N')
    axis[0].spines['right'].set_visible(False)
    axis[0].spines['top'].set_visible(False)

    if PLOT_PARAMETERS:
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

        Graph.plot_table_params(ax=axis[2], params_dict=table_params)

    iteration = 0
    for dt in range(2000):
        society.make_step()

        if iteration == 0 or (iteration == 10):
            axis[0].clear()

            society_status = society.get_status()
            cumulative_status = society.get_cumulative_status()


            times.append(time / 3600 / 24)
            for st in Status:
                #society_progress[st.name].append(society_status[st.name] / society_status["Total"])
                society_progress[st.name].append(cumulative_status[st.name])
                #axis[0].plot(times, society_progress[st.name], c=st.value, ls='-', label=st.name)

            axis[0].fill_between(
                times, 0, society_progress[Status.Infected.name],
                color=Status.Infected.value,
                label=Status.Infected.name,
                alpha=0.7
            )

            axis[0].fill_between(
                times, society_progress[Status.Infected.name], society_progress[Status.Healthy.name],
                color=Status.Healthy.value,
                label=Status.Healthy.name,
                alpha=0.7
            )

            axis[0].fill_between(
                times, society_progress[Status.Healthy.name], society_progress[Status.Immune.name],
                color=Status.Immune.value,
                label=Status.Immune.name,
                alpha=0.7
            )

            axis[0].fill_between(
                times, society_progress[Status.Immune.name], society_progress[Status.Confined.name],
                color=Status.Confined.value,
                label=Status.Confined.name,
                alpha=0.7
            )

            axis[0].text(
                times[-1], 1/2 *(0 + cumulative_status[Status.Infected.name]),
                r"{0:.2f}".format(society_status[Status.Infected.name] / len(society.agents)),
                size=10,
                color=Status.Infected.value
            )

            # axis[0].text(
            #     times[-1], 1/2 * (society_status[Status.Infected.name] + society_status[Status.Infected.name]) / 2,
            #     r"{0:.2f}".format(society_progress[Status.Healthy.name][-1]),
            #     size=10,
            #     color=Status.Healthy.value
            # )
            #
            # axis[0].text(
            #     times[-1], (healthy_level[-1] + immune_level[-1]) / 2,
            #     r"{0:.2f}".format(society_progress[Status.Immune.name][-1]),
            #     size=10,
            #     color=Status.Immune.value
            # )
            #
            # axis[0].text(
            #     times[-1], (immune_level[-1] + confined_level[-1]) / 2,
            #     r"{0:.2f}".format(society_progress[Status.Confined.name][-1]),
            #     size=10,
            #     color=Status.Confined.value
            # )

            axis[0].set_ylim(0, Geometry.Box.Ly)
            axis[0].legend(loc=2)

            society.plot(axis[1])

            plt.show()
            logger.info(f"| {time / 3600}h - "
                        f"infected: {society_status[Status.Infected.name]}, "
                        f"healthy: {society_status[Status.Healthy.name]}, "
                        f"immune: {society_status[Status.Immune.name]}, "
                        f"confined: {society_status[Status.Confined.name]}")

        # if iteration == 0:
        #     axis[0].legend(loc=2)

        if iteration == 0 or (iteration == 10):
            iteration = 1
            plt.pause(0.001)

        time += Time.STEP_SEC
        iteration += 1

    plt.show()
    plt.pause(60)


if __name__ == "__main__":

    run()

