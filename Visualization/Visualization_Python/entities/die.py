from utils.types_name import DIE
from entities.component import Component
from entities.quad import Quad
from typing import Dict, Any
from utils.constants import *


class Die(Component):
    def __init__(self, id: int, data: Dict[str, Any]):
        super().__init__(id, DIE)
        self.quads = [[None for _ in range(2)] for _ in range(2)]
        self.data = data
        self.init_quads()
        self.is_enable = False

    # Initializing the quads belonging to the die and inserting them into the quads matrix
    def init_quads(self) -> None:
        quads = self.data.get(GRID, {}).get(QUADS, [])

        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]

        for index, quad_data in enumerate(quads):
            pos = positions[index % len(positions)]
            row, col = pos

            new_quad = Quad(quad_data.get(ID), quad_data.get(NAME), quad_data)

            self.quads[row][col] = new_quad

    def get_attribute_from_active_logs(self,attribute):
        attributes=[]
        for row in self.quads:
            for quad in row:
                    attributes.extend(quad.get_attribute_from_active_logs(attribute))
            attributes.extend(super().get_attribute_from_active_logs(attribute))
        return attributes