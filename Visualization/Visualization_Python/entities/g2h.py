from utils.types_name import IRQA
from entities.component import Component
from utils.constants import *
from typing import Dict, Any, List


class G2h(Component):
    def __init__(self, id: int, type: str, data: Dict[str, Any]):
        super().__init__(id, type)
        self.data = data
        self.g2h_irqa = Component(None, IRQA)
        self.eqs = []

        self.init_eqs()

    # Initializing the eqs belonging to the g2h and inserting them into the eqs list
    def init_eqs(self) -> None:
        for eq in self.data[EQS]:
            eq = Component(eq[ID], EQ)
            self.eqs.append(eq)

    # The function returns the elements in the g2h
    def get_details(self) -> List[Component]:
        return [self.g2h_irqa]+self.eqs

    def get_attribute_from_active_logs(self, attribute):
        attributes = []
        for inner_obj in self.get_details():
            attributes.extend(inner_obj.get_attribute_from_active_logs(attribute))
        attributes.extend(super().get_attribute_from_active_logs(attribute))
        return attributes
