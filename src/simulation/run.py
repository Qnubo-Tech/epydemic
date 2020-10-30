import logging
import matplotlib.pyplot as plt
import numpy as np

from src.environment.society import Society
from src.environment.status import Status
from src.geometry.geometry import Geometry

from src.simulation import (
    Graph, Time, TimeConverter,
    DiseaseParams,
    ImmunityParams,
    InfectionParams,
    POPULATION, HEALTHY_PC, INFECTED_PC,
    PLOT_PARAMETERS
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

np.random.seed(72)


def run():

    society = Society(
        population=POPULATION,
        initial_condition={"healthy": HEALTHY_PC, "infected": INFECTED_PC}
    )

    plt.ion()

    fig, axis = Graph.generate_fig_ax(show_params=PLOT_PARAMETERS)

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
            "Mean recovery time [days]": InfectionParams.RECOVERY_TIME_DAYS,
            "Mean immunity shield [days]": ImmunityParams.SHIELD_TIME_DAYS,
            "Immunity probability": ImmunityParams.PROBABILITY,
            "Loss immunity probability": ImmunityParams.LOSS_PROBABILITY,
            "Confined probability": InfectionParams.CONFINED_PROBABILITY,
            "Viral stickiness": DiseaseParams.VIRAL_STICKINESS
        }

        Graph.plot_table_params(ax=axis[2], params_dict=table_params)

    iteration = 0
    for dt in range(2000):
        society.make_step()

        if iteration == 0 or (iteration == 10):
            axis[0].clear()

            society_status = society.get_status()
            cumulative_status = society.get_cumulative_status()

            times.append(time / TimeConverter.DAY_TO_SEC)
            # Graph.plot_areas_society_progress(ax=axis[0],
            #                                   time_array=times,
            #                                   society_snapshot=cumulative_status,
            #                                   society_progress=society_progress)
            Graph.plot_lines_society_progress(ax=axis[0],
                                              time_array=times,
                                              society_snapshot=society_status,
                                              society_progress=society_progress)

            axis[0].set_ylim(0, Geometry.Box.Ly)
            axis[0].legend(loc=2)

            society.plot(axis[1])

            plt.show()
            logger.info(f"| {time / TimeConverter.HOUR_TO_SEC} h - "
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

