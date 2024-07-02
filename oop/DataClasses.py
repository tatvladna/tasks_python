from functools import total_ordering


@total_ordering
class Shape:
    __slots__ = ('name', 'color', 'area')

    def __init__(self, name, color, area):
        self.name = name
        self.color = color
        self.area = area

    def __str__(self):
        return f"{self.color} {self.name} ({self.area})"

    def __eq__(self, other):
        if isinstance(other, Shape):
            return self.area == other.area
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Shape):
            return self.area > other.area
        return NotImplemented



# shape = Shape('triangle', 'red', 12)
#
# try:
#     shape.perimeter = 9
# except AttributeError:
#     print('Error')

####################
#using dataclasses
from dataclasses import dataclass, field

@dataclass(frozen=True, order=True)
class Shape:
    name: str = field(compare=False)
    color: str = field(compare=False)
    area: int = field(compare=True)

    def __str__(self):
        return f"{self.color} {self.name} ({self.area})"



shape = Shape('triangle', 'red', 12)

try:
    shape.perimeter = 9
except AttributeError:
    print('Error')