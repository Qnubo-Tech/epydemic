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
            previous_status = None
            for st in Status:
                # lines
                #society_progress[st.name].append(society_status[st.name] / society_status["Total"])
                #axis[0].plot(times, society_progress[st.name], c=st.value, ls='-', label=st.name)

                # stacked areas
                society_progress[st.name].append(cumulative_status[st.name])

                if previous_status:
                    lower_limit = society_progress[previous_status.name]
                else:
                    lower_limit = [0]

                axis[0].fill_between(
                    x=times, y1=lower_limit, y2=society_progress[st.name],
                    color=st.value, label=st.name, alpha=0.25
                )

                axis[0].text(
                    x=times[-1], y=1/2 * (lower_limit[-1] + cumulative_status[st.name]),
                    s=r"{0:.2f}".format(cumulative_status[st.name] - lower_limit[-1]),
                    size=10,
                    color=st.value
                )

                previous_status = st

            axis[0].set_ylim(0, Geometry.Box.Ly)
            axis[0].legend(loc=2)

            society.plot(axis[1])

            plt.show()
            logger.info(f"| {time / 3600}h - "
                        f"infected: {society_status[Status.Infected.name]}, "
                        f"healthy: {society_status[Status.Healthy.name]}, "
                        f"immune: {society_status[Status.Immune.name]}, "
                        f"confined: {society_status[Status.Confined.name]}")

        if iteration == 0 or (iteration == 10):
            iteration = 1
            plt.pause(0.001)

        time += Time.STEP_SEC
        iteration += 1

    plt.show()
    plt.pause(60)


if __name__ == "__main__":

    run()

