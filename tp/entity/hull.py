from tp.util import Polygon, meters, kilograms

"""
Requirements:
Hull shape must be:
    1. symmetrical
    2. convex
    3. points in counter-clockwise order
    4. start with (0.0, 0.0)
    5. defined in millimeters.

The position (0.0, 0.0) will serve as the top center part of the hull, which will extend downwards.
"""


class Hull(object):
    def __init__(self,
                 cross_sec_shape: Polygon,
                 length: meters,
                 mass: kilograms):
        assert len(cross_sec_shape) >= 3
        assert length > 0.0
        assert mass > 0.0

        self.cross_sec_shape = cross_sec_shape
        self.length = length
        self.mass = mass
