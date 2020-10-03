import random

import matplotlib.pyplot as plt
import numpy as np


from src.geometry import Geometry
from src.environment import Agent, Status


class Society:

    def __init__(self, population, volume):

        self.population = population
        self.volume = volume
        self.agents = self._create_agents()

    def _create_agents(self):

        agents = []

        for i in range(self.population):

            agents.append(
                Agent(x=random.uniform(0, Geometry.Box.Lx),
                      y=random.uniform(0, Geometry.Box.Ly),
                      status=np.random.choice([Status.Infected, Status.Healthy], p=[0.01, 0.99]),
                      mobility=0.0001
                      )
            )

        return agents

    def make_step(self):

        [agent.step(force=self.force_field(agent.position)) for agent in self.agents]

    def force_field(self, position):

        return np.sum([agent.viral_force(position) for agent in self.agents])

    def compute_field(self, mesh):

        aux_f = [
            self.force_field(position=np.array([x, y]))
            for j, y in enumerate(mesh.y_range)
            for i, x in enumerate(mesh.x_range)
        ]

        return np.array(aux_f).reshape(mesh.x_range.size, mesh.y_range.size)

    def plot_field(self, ax, mesh):

        f = self.compute_field(mesh)

        ax.clear()
        ax.contour(mesh.X, mesh.Y, f)
        ax.set_aspect('equal')

    def plot(self, ax):

        ax.clear()
        [(
            ax.scatter(agent.x, agent.y, s=5, color=agent.status.value),
            ax.add_artist(plt.Circle((agent.x, agent.y),
                                     radius=agent.disease.infection_radius,
                                     color=agent.status.value,
                                     alpha=0.5*agent.viral_load))
         )
            for agent in self.agents
        ]
        ax.set_xlim(0, Geometry.Box.Lx)
        ax.set_ylim(0, Geometry.Box.Ly)
        ax.set_aspect('equal')

    def count_statuses(self, status: Status):
        return len([1 for agent in self.agents if (agent.status == status)])

    def get_status(self):
        n_healthy = self.count_statuses(Status.Healthy)
        n_infected = self.count_statuses(Status.Infected)
        n_immune = self.count_statuses(Status.Immune)
        total = sum([n_healthy, n_infected, n_immune])
        return {'healthy': n_healthy, 'infected': n_infected, 'immune': n_immune, 'total': total}