import time

import matplotlib.pyplot as plt

from src.society import Society, Geometry


def run():

    society = Society(population=62, volume=1)

    fig, ax = plt.subplots()
    society.plot_field(ax=ax, mesh=Geometry.Box)

    plt.show()

    fig, ax = plt.subplots()
    society.plot(ax=ax)

    plt.show()

    # plt.ion()
    # fig, ax = plt.subplots()
    #
    # for i in range(500):
    #     society.make_step()
    #     society.plot(ax)
    #     ax.set_title(f"Days={i / 24}")
    #     plt.pause(0.01)
    #
    #
    # plt.show()


if __name__ == "__main__":

    run()

