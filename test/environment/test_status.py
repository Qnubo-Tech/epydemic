import pytest

from src.environment.status import Status


@pytest.fixture(scope="module")
def status_dict():
    st_dict = {
        "Infected": "red",
        "Healthy": "blue",
        "Immune": "darkgreen",
        "Confined": "orange"
    }
    return st_dict


def test_names(status_dict):
    for st in status_dict.keys():
        assert st in Status.__members__


def test_values(status_dict):
    for k, v in status_dict.items():
        assert v == Status[k].value
