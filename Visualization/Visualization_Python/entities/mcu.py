from utils.types_name import *
from entities.component import Component
from utils.constants import *
from typing import Dict, Any, List


class Mcu(Component):
    def __init__(self, id: int, type: str, data: Dict[str, Any]):
        super().__init__(id, type)
        self.mcu_irqa = Component(None, IRQA)
        self.iqr = Component(None, IQR)
        self.iqd = Component(None, IQD)
        self.bin = Component(None, BIN)
        self.data = data
        self.eqs = []

        self.init_eqs()

    # Initializing the eqs belonging to the mcu and inserting them into the eqs list
    def init_eqs(self) -> None:
        for eq in self.data[EQS]:
            eq = Component(eq[ID], EQ)
            self.eqs.append(eq)

    def get_details(self) -> List[Component]:
        return [self.mcu_irqa, self.iqr, self.iqd,self.bin] + self.eqs

    def get_attribute_from_active_logs(self, attribute):
        attributes = []
        for inner_obj in self.get_details():
            attributes.extend(inner_obj.get_attribute_from_active_logs(attribute))
        attributes.extend(super().get_attribute_from_active_logs(attribute))
        return attributes
