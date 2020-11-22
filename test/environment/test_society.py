import pytest

import numpy as np
from numpy.testing import assert_array_equal

from src.configuration import ConfinementParams, DiseaseParams
from src.environment import Society, Status
from src.geometry import Box


@pytest.fixture()
def society() -> Society:
    return Society(
        population=10,
        initial_condition={Status.Healthy.name: 0.9, Status.Infected.name: 0.1}
    )


@pytest.fixture()
def infected_society() -> Society:
    society = Society(
        population=10,
        initial_condition={Status.Healthy.name: 0, Status.Infected.name: 1}
    )

    positions = np.linspace(0, 0.9, 10)
    positions[1] = DiseaseParams.INFECTION_RADIUS / 2
    for i, y in enumerate(positions):
        society.agents[i].position = np.array([0, y])

    return society


def test_initial_params(society):
    assert society.population == 10
    assert len(society.agents) == 10
    assert society.num_infected == 1
    assert society.num_healthy == 9
    assert society.num_immune == 0
    assert society.num_confined == 0
    assert society.confined_share == 0
    assert society.t_simulation == 0


def test_count_statuses(society):
    infected = len([1 for agent in society.agents if agent.status == Status.Infected])
    healthy = len([1 for agent in society.agents if agent.status == Status.Healthy])
    immune = len([1 for agent in society.agents if agent.status == Status.Immune])
    confined = len([1 for agent in society.agents if agent.status == Status.Confined])
    assert society.count_statuses(status=Status.Infected) == infected
    assert society.count_statuses(status=Status.Healthy) == healthy
    assert society.count_statuses(status=Status.Immune) == immune
    assert society.count_statuses(status=Status.Confined) == confined


def test_get_status(society):
    society_status = {
        Status.Infected.name: 1,
        Status.Healthy.name: 9,
        Status.Immune.name: 0,
        Status.Confined.name: 0,
        "Total": 10
    }
    assert society.get_status() == society_status


def test_get_stacked_status(society):
    society_status = {
        Status.Infected.name: 0.1,
        Status.Healthy.name: 1.0,
        Status.Immune.name: 1.0,
        Status.Confined.name: 1.0
    }
    assert society.get_stacked_status() == society_status


def test_set_confinement_eligibility_no_eligibles(society):
    num_confined = round(ConfinementParams.CONFINEMENT_CAPACITY * society.population) + 1
    for i in range(num_confined):
        society.agents[i].status = Status.Confined

    society._set_confinement_eligibility()

    assert society.confined_share > ConfinementParams.CONFINEMENT_CAPACITY
    assert all([agent.allow_confinement is False for agent in society.agents])


def test_set_confinement_eligibility(society):
    society._set_confinement_eligibility()

    eligible_share = int(society.population * ConfinementParams.ELIGIBLE_POPULATION_SHARE)
    confinement_eligible_agents = [
        1 if agent.allow_confinement is True else 0
        for agent in society.agents
    ]

    assert sum(confinement_eligible_agents) == eligible_share


def test_force_field(infected_society):
    epsilon = 1e-6

    zero_force_position = np.array([0, infected_society.agents[-1].y +
                                    DiseaseParams.INFECTION_RADIUS +
                                    epsilon])
    one_force_position = np.array([0, infected_society.agents[-1].y +
                                   DiseaseParams.INFECTION_RADIUS -
                                   epsilon])
    double_force_position = np.array([0, (infected_society.agents[0].y +
                                          infected_society.agents[1].y) / 2])

    assert infected_society.force_field(position=zero_force_position) == 0
    assert infected_society.force_field(position=one_force_position) == 1.
    assert infected_society.force_field(position=double_force_position) == 2


def test_compute_field(infected_society):
    expected_field = np.zeros(shape=(Box.x_range().size, Box.y_range().size))
    expected_field[:, 0] = np.array([
        infected_society.force_field(position=np.array([Box.x_range()[0], y]))
        for y in Box.y_range()
    ])
    expected_field[:, 1] = np.array([
        infected_society.force_field(position=np.array([Box.x_range()[1], y]))
        for y in Box.y_range()
    ])

    assert_array_equal(infected_society.compute_field(mesh=Box), expected_field)

