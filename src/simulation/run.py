import matplotlib.pyplot as plt

from src.environment import Status, Society
from src.simulation import Time

def run():

    society = Society(population=100, volume=1)

    # plt.ion()
    # fig, ax = plt.subplots()
    # society.plot_field(ax=ax, mesh=Geometry.Box)
    # plt.show()
    #
    # fig, ax = plt.subplots()
    # society.plot(ax=ax)
    # plt.show()

    # plt.ion()
    # fig, ax = plt.subplots()
    #
    # legend_elements = [ax.scatter(0, 0, s=5, color=e.value, label=e.name) for e in Status]
    #
    # for i in range(500):
    #     society.make_step()
    #     society.plot(ax)
    #     ax.set_title(f"Days={i // 24}")
    #     ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.05, 1))
    #     plt.pause(0.01)
    #
    # plt.show()

    plt.ion()
    fig, ax = plt.subplots()

    immune, infected, healthy, times = ([],[],[], [])
    time = 0

    plt.xlabel('time / days')
    plt.ylabel('N')

    iteration = 0
    for dt in range(2000):
        society.make_step()
        res = society.get_status()

        immune.append(res['immune'])
        healthy.append(res['healthy'])
        infected.append(res['infected'])
        times.append(time / 3600 / 24)

        if iteration == 0 or (iteration == 10):
            ax.plot(times, healthy, c=Status.Healthy.value, marker="^", ls='--', label='Healthy',)
            ax.plot(times, infected, c=Status.Infected.value, marker="o", ls='-', label='Infected')
            ax.plot(times, immune, c=Status.Immune.value, marker="v", ls=':', label='Immmune')
            plt.show()
            print(f'{time / 3600}h / {iteration} | inf: {res["infected"]}, hea: {res["healthy"]}, imm: {res["immune"]}')

        if iteration == 0:
            ax.legend(loc=2)

        if iteration == 0 or (iteration == 10):
            iteration = 1
            plt.pause(0.01)

        time += Time.STEP_SEC
        iteration += 1

    plt.show()
    plt.pause(60)


if __name__ == "__main__":

    run()

