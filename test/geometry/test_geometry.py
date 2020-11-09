import numpy as np
from numpy.testing import assert_array_equal

from src.geometry import Box


def test_box():
    default_x = Box.Lx
    default_y = Box.Ly

    limit = 10

    Box.Lx = limit
    Box.Ly = limit

    assert Box.Lx == limit
    assert Box.Ly == limit
    assert_array_equal(Box.x_range(), np.linspace(0, limit, 100))
    assert_array_equal(Box.y_range(), np.linspace(0, limit, 100))
    assert_array_equal(Box.x_y(),
                       np.meshgrid(np.linspace(0, limit, 100), np.linspace(0, limit, 100)))
    assert Box.x_limits() == [0, limit]
    assert Box.x_limits() == [0, limit]

    Box.Lx = default_x
    Box.Ly = default_y
