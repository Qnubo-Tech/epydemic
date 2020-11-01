import numpy as np
from numpy.testing import assert_array_equal

from src.geometry.geometry import Geometry


def test_box():
    default_x = Geometry.Box.Lx
    default_y = Geometry.Box.Ly

    limit = 10

    Geometry.Box.Lx = limit
    Geometry.Box.Ly = limit

    assert Geometry.Box.Lx == limit
    assert Geometry.Box.Ly == limit
    assert_array_equal(Geometry.Box.x_range(), np.linspace(0, limit, 100))
    assert_array_equal(Geometry.Box.y_range(), np.linspace(0, limit, 100))
    assert_array_equal(Geometry.Box.x_y(),
                       np.meshgrid(np.linspace(0, limit, 100), np.linspace(0, limit, 100)))
    assert Geometry.Box.x_limits() == [0, limit]
    assert Geometry.Box.x_limits() == [0, limit]

    Geometry.Box.Lx = default_x
    Geometry.Box.Ly = default_y
