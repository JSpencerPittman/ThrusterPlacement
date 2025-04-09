from tp.entity import Hull
from tp.util import meters, kilograms


class Boat(object):
    def __init__(self,
                 deck_mass: kilograms,
                 hulls: list[Hull],
                 hull_separation: meters = 0.0):
        self.deck_mass = deck_mass
        self.hulls = hulls

        if len(hulls) > 1:
            assert hull_separation != 0

    @property
    def num_hulls(self) -> int:
        return len(self.hulls)

    @property
    def total_weight(self) -> kilograms:
        cum_hull_mass = sum([hull.mass for hull in self.hulls])
        return self.deck_mass + cum_hull_mass
