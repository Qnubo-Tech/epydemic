import matplotlib.pyplot as plt

from src.environment import Status, Society


def run():

    society = Society(population=50, volume=1)

    # fig, ax = plt.subplots()
    # society.plot_field(ax=ax, mesh=Geometry.Box)
    #
    # plt.show()
    #
    # fig, ax = plt.subplots()
    # society.plot(ax=ax)

    #plt.show()

    plt.ion()
    fig, ax = plt.subplots()

    legend_elements = [ax.scatter(0, 0, s=5, color=e.value, label=e.name) for e in Status]

    for i in range(500):
        society.make_step()
        society.plot(ax)
        ax.set_title(f"Days={i // 24}")
        ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.05, 1))
        plt.pause(0.01)

    plt.show()


if __name__ == "__main__":

    run()

