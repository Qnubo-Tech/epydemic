import matplotlib.pyplot as plt

from src.environment import Status, Society
from src.simulation import Time
from src.geometry.geometry import Geometry

def run():

    society = Society(
        population=54, volume=1, initial_condition={'healthy': 0.99, 'infected': 0.01}
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
    fig, (ax1, ax2) = plt.subplots(1, 2)

    immune, infected, healthy, times = ([],[],[], [])
    time = 0

    plt.xlabel('time / days')
    plt.ylabel('N')

    iteration = 0
    for dt in range(2000):
        society.make_step()

        if iteration == 0 or (iteration == 10):
            res = society.get_status()
            immune.append(res['immune'] / res['total'])
            healthy.append(res['healthy'] / res['total'])
            infected.append(res['infected'] / res['total'])
            times.append(time / 3600 / 24)

            ax1.plot(times, healthy, c=Status.Healthy.value, ls='--', label='Healthy',)
            ax1.plot(times, infected, c=Status.Infected.value, marker="o", ls='-', label='Infected')
            ax1.plot(times, immune, c=Status.Immune.value, ls=':', label='Immmune')

            ax1.set_ylim(0, Geometry.Box.Ly)

            society.plot(ax2)

            plt.show()
            print(f'{time / 3600}h / {iteration} | inf: {res["infected"]}, hea: {res["healthy"]}, imm: {res["immune"]}')

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

