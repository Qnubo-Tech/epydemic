import pytest

import numpy as np

from src.configuration import Time

from src.environment.agent import Agent
from src.environment.mobility import MobilityType
from src.environment.status import Status

from src.geometry import Box


@pytest.fixture()
def agent() -> Agent:
    agent = Agent(x=0.,
                  y=0.,
                  mobility_value=0.0001,
                  mobility_type=MobilityType.unlimited,
                  status=Status.Healthy)
    return agent


@pytest.fixture()
def infected_agent() -> Agent:
    agent = Agent(x=0.,
                  y=0.,
                  mobility_value=0.0001,
                  mobility_type=MobilityType.unlimited,
                  status=Status.Infected)
    return agent


def test_initial_values(agent):
    assert agent.position.size == 2
    assert agent.position[0] == 0
    assert agent.position[1] == 0
    assert agent.mobility.value == 0.0001
    assert agent.status == Status.Healthy
    assert agent.disease.viral_load == 0
    assert agent.t_alive == 0
    assert agent.x == 0
    assert agent.y == 0
    assert agent.viral_load == 0
    assert agent.mobility_args == {"time_alive": 0}


def test_set_initial_viral_load_not_infected(agent):
    assert agent._set_initial_viral_load() == 0


def test_set_initial_viral_load_infected(infected_agent):
    assert infected_agent._set_initial_viral_load() == 1


def test_apply_boundary_conditions(agent):
    agent.position = np.array([Box.Lx * 1.5, Box.Ly * 1.5])
    agent._apply_boundary_conditions()
    assert 0 <= agent.position[0] <= Box.Lx
    assert 0 <= agent.position[1] <= Box.Ly


def test_viral_force(infected_agent):
    distant_position = np.array([1, 1])
    same_position = np.array([0, 0])
    close_position = np.array([0, 0.01])

    assert infected_agent.viral_force(position=distant_position) == 0
    assert infected_agent.viral_force(position=same_position) == 0
    assert infected_agent.viral_force(position=close_position) == infected_agent.viral_load


def test_step(agent):
    agent.step(force=0)
    assert agent.viral_load == 0
    assert 0 <= agent.x <= Box.Lx
    assert 0 <= agent.y <= Box.Ly
    assert agent.t_alive == Time.STEP_SEC


def test_step_confined_agent(agent):
    agent.status = Status.Confined
    agent.step(force=0)
    assert agent.x == -1
    assert agent.y == -1
    assert agent.t_alive == Time.STEP_SEC
