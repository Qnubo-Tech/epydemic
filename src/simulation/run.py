import logging
import matplotlib.pyplot as plt
import numpy as np

from src.environment import Society
from src.environment.status import Status
from src.geometry import Box

from src.configuration import (
    Time, TimeConverter,
    SocietyParams,
    DiseaseParams,
    ImmunityParams,
    InfectionParams,
    PLOT_PARAMETERS
)

from src.simulation import Graph

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

np.random.seed(72)


def run():

    society = Society(
        population=SocietyParams.POPULATION,
        initial_condition={
            Status.Healthy.name: SocietyParams.HEALTHY_PC,
            Status.Infected.name: SocietyParams.INFECTED_PC
        }
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
            "Population": SocietyParams.POPULATION,
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
            cumulative_status = society.get_stacked_status()

            times.append(time / TimeConverter.DAY_TO_SEC)
            # Graph.plot_areas_society_progress(ax=axis[0],
            #                                   time_array=times,
            #                                   society_snapshot=cumulative_status,
            #                                   society_progress=society_progress)
            Graph.plot_lines_society_progress(ax=axis[0],
                                              time_array=times,
                                              society_snapshot=society_status,
                                              society_progress=society_progress)

            axis[0].set_ylim(0, Box.Ly)
            axis[0].legend(loc=2)

            society.plot(axis[1])

            plt.show()
            logger.info(f"| {time / TimeConverter.HOUR_TO_SEC} h - "
                        f"infected: {society.num_infected}, "
                        f"healthy: {society.num_healthy}, "
                        f"immune: {society.num_immune}, "
                        f"confined: {society.num_confined}")

        if iteration == 0 or (iteration == 10):
            iteration = 1
            plt.pause(0.001)

        time += Time.STEP_SEC
        iteration += 1

    plt.show()
    plt.pause(60)


if __name__ == "__main__":

    run()

